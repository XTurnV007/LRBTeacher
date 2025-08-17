import os
import requests
import json
import numpy as np
import streamlit as st
import faiss
import chardet
import fitz  # PyMuPDF
from typing import List, Tuple
from utils.config_manager import get_api_keys
from utils.i18n import t

def get_api_key():
    """获取API密钥"""
    keys = get_api_keys()
    return keys.get("openai_api_key", "")
EMBEDDING_MODEL = "embedding-2"
EMBEDDING_API_URL = "https://open.bigmodel.cn/api/paas/v4/embeddings"
VECTOR_DIMENSION = 1024
EMBEDDING_FILE = "embeddings.txt"

def get_embedding(text: str) -> List[float]:
    api_key = get_api_key()
    if not api_key:
        raise ValueError("请在配置面板中设置OpenAI API密钥")
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    payload = {
        "model": EMBEDDING_MODEL,
        "input": text
    }
    response = requests.post(EMBEDDING_API_URL, headers=headers, data=json.dumps(payload))
    response.raise_for_status()
    data = response.json()
    return data["data"][0]["embedding"]

def get_embeddings_for_long_text(text: str) -> List[float]:
    max_length = 512
    segments = [text[i:i+max_length] for i in range(0, len(text), max_length)]
    embeddings = []
    for segment in segments:
        embedding = get_embedding(segment)
        embeddings.append(embedding)
    avg_embedding = np.mean(embeddings, axis=0).tolist()
    return avg_embedding

def store_embeddings_to_file(embeddings: List[Tuple[str, List[float]]], file_path: str):
    with open(file_path, 'w', encoding='utf-8') as f:
        for text, embedding in embeddings:
            f.write(f"{text}\t{json.dumps(embedding)}\n")

def load_embeddings_from_file(file_path: str) -> List[Tuple[str, List[float]]]:
    embeddings = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            text, embedding = line.strip().split('\t')
            embeddings.append((text, json.loads(embedding)))
    return embeddings

def build_faiss_index(embeddings: List[Tuple[str, List[float]]]) -> faiss.IndexFlatL2:
    index = faiss.IndexFlatL2(VECTOR_DIMENSION)
    vectors = np.array([embedding for _, embedding in embeddings]).astype('float32')
    index.add(vectors)
    return index

def search_similar_texts(query_embedding: List[float], embeddings: List[Tuple[str, List[float]]], index: faiss.IndexFlatL2, top_k: int = 5) -> List[Tuple[str, float]]:
    query_vector = np.array(query_embedding).reshape(1, -1).astype('float32')
    distances, indices = index.search(query_vector, top_k)
    return [(embeddings[idx][0], distances[0][i]) for i, idx in enumerate(indices[0])]

def read_file_content(uploaded_file):
    raw_data = uploaded_file.read()
    result = chardet.detect(raw_data)
    encoding = result['encoding'] if result['encoding'] else 'utf-8'
    return raw_data.decode(encoding, errors='ignore')

def read_pdf_content(uploaded_file):
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    content = ""
    for page in doc:
        content += page.get_text()
    return content

def knowledge_base_management_method():
    st.title(t('knowledge_base_management'))
    option = st.selectbox(t('select_operation'), [t('upload_files'), t('search_files'), t('view_knowledge_base')])
    
    if option == t('upload_files'):
        uploaded_files = st.file_uploader(t('choose_files_to_upload'), accept_multiple_files=True, type=["txt", "pdf"])
        if st.button(t('process_files')):
            if uploaded_files:
                embeddings = []
                with st.spinner(t('processing_files')):
                    for uploaded_file in uploaded_files:
                        try:
                            if uploaded_file.name.endswith(".pdf"):
                                content = read_pdf_content(uploaded_file)
                            else:
                                content = read_file_content(uploaded_file)
                            embedding = get_embeddings_for_long_text(content)
                            embeddings.append((uploaded_file.name, embedding))
                            st.success(t('file_processed', uploaded_file.name))
                        except Exception as e:
                            st.error(t('file_processing_error', uploaded_file.name, str(e)))
                if embeddings:
                    store_embeddings_to_file(embeddings, EMBEDDING_FILE)
                    st.success(t('all_files_processed'))
            else:
                st.warning(t('please_upload_files'))
    
    elif option == t('search_files'):
        query_text = st.text_input(t('enter_query_text'))
        if st.button(t('search')):
            if query_text:
                with st.spinner(t('searching')):
                    embeddings = load_embeddings_from_file(EMBEDDING_FILE)
                    index = build_faiss_index(embeddings)
                    query_embedding = get_embeddings_for_long_text(query_text)
                    results = search_similar_texts(query_embedding, embeddings, index)
                    st.write(t('search_results'))
                    for result in results:
                        st.write(f"{t('filename')} {result[0]}, {t('similarity')} {result[1]}")
            else:
                st.warning(t('please_enter_query'))
    
    elif option == t('view_knowledge_base'):
        embeddings = load_embeddings_from_file(EMBEDDING_FILE)
        st.write(t('existing_knowledge_base'))
        for text, _ in embeddings:
            st.write(f"{t('filename')} {text}")

def search_local_knowledge_base(query_embedding: List[float], top_k: int = 5) -> List[Tuple[str, float]]:
    embeddings = load_embeddings_from_file(EMBEDDING_FILE)
    index = build_faiss_index(embeddings)
    return search_similar_texts(query_embedding, embeddings, index, top_k)

