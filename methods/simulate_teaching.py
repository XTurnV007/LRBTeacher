import json
import streamlit as st
from zhipuai import ZhipuAI
from config.config import DEFAULT_MODEL
from utils.chat_helpers import add_to_chat_history, build_prompt, clean_api_response, generate_image_url, generate_content
from utils.css_styles import persona_card_styles
from utils.api_client import get_api_client
import time

def generate_persona(user_input):
    prompt = build_prompt(user_input)
    client = get_api_client()
    response = client.chat.completions.create(
        model=DEFAULT_MODEL,
        messages=[{'role': 'user', 'content': prompt}]
    )

    result = ""
    try:
        if hasattr(response, 'choices'):
            for choice in response.choices:
                if hasattr(choice, 'message'):
                    cleaned_content = clean_api_response(choice.message.content)
                    result += cleaned_content
    except Exception as e:
        st.error(f"Error processing response: {e}")

    add_to_chat_history('assistant', result)
    return result

def generate_notes_stream(persona, topic):
    prompt = f"基于以下人设生成关于'{topic}'的小红书笔记：{persona}；要求：有个性，不需要罗列很多点。"
    client = get_api_client()
    response = client.chat.completions.create(
        model=DEFAULT_MODEL,
        messages=[{'role': 'user', 'content': prompt}],
        stream=True  # 开启流式响应
    )

    result = ""
    try:
        for chunk in response:
            if chunk == "[DONE]":
                break
            if hasattr(chunk, 'choices') and chunk.choices:
                delta = chunk.choices[0].delta
                if delta and hasattr(delta, 'content') and delta.content:
                    content = delta.content
                    result += content
                    yield content  # 实时返回生成的内容
    except Exception as e:
        st.error(f"Error processing response: {e}")

    return result

def sync_session_state():
    if 'personas' not in st.session_state:
        st.session_state.personas = []
    if 'show_input' not in st.session_state:
        st.session_state.show_input = []
    if 'notes' not in st.session_state:
        st.session_state.notes = []

    # Ensure lengths are the same
    while len(st.session_state.show_input) < len(st.session_state.personas):
        st.session_state.show_input.append(False)
    while len(st.session_state.notes) < len(st.session_state.personas):
        st.session_state.notes.append("")

    # In case the lists are longer than personas (which shouldn't happen but just in case)
    while len(st.session_state.show_input) > len(st.session_state.personas):
        st.session_state.show_input.pop()
    while len(st.session_state.notes) > len(st.session_state.personas):
        st.session_state.notes.pop()

def simulate_teaching_method():
    st.title("模拟教学方法")

    if 'css_styles_loaded' not in st.session_state:
        st.markdown(persona_card_styles, unsafe_allow_html=True)
        st.session_state['css_styles_loaded'] = True

    st.markdown(
        """
        <style>
        .description {
            font-size: 16px;
            color: #4a4a4a;
            margin-top: -15px;
            margin-bottom: 30px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # 详细描述
    st.markdown('<p class="description">方法简介：可以模拟小红书创建账号人设，并根据主题词和人设撰写小红书笔记。</p>', unsafe_allow_html=True)

    global content_topic

    st.write("请输入内容主题：")
    content_topic_input = st.text_input("内容主题", key="content_topic_input")

    if st.button("生成人设"):
        content_topic = content_topic_input
        with st.spinner("正在生成人设..."):
            persona = generate_persona(content_topic_input)
            print(persona)
            image_url = generate_image_url(persona)
            if 'personas' not in st.session_state:
                st.session_state.personas = []
            st.session_state.personas.append((persona, image_url))
            sync_session_state()

    if 'personas' in st.session_state:
        st.markdown(persona_card_styles, unsafe_allow_html=True)
        for idx, (persona, image_url) in enumerate(st.session_state.personas):
            create_persona_card(persona, image_url, idx)
        st.markdown("</div>", unsafe_allow_html=True)

def create_persona_card(description, image_url, idx):
    def build_html_content(data):
        def generate_list(data):
            if isinstance(data, dict):
                items = ""
                for key, value in data.items():
                    if isinstance(value, (dict, list)):
                        items += f"<li><strong>{key}:</strong>{generate_list(value)}</li>"
                    else:
                        items += f"<li><strong>{key}:</strong> {value}</li>"
                return f"<ul>{items}</ul>"
            elif isinstance(data, list):
                items = ""
                for item in data:
                    if isinstance(item, (dict, list)):
                        items += f"<li>{generate_list(item)}</li>"
                    else:
                        items += f"<li>{item}</li>"
                return f"<ul>{items}</ul>"
            else:
                return f"<li>{data}</li>"

        return generate_list(data)

    try:
        persona_data = json.loads(description)
    except json.JSONDecodeError:
        persona_data = {"description": description}

    card_html_content = build_html_content(persona_data)

    st.markdown(
        f"""
        <div class="persona-card">
            <h5>人设卡片</h5>
            <img src="{image_url}" class="persona-avatar" alt="Avatar">
            <div style="height: auto; overflow: hidden; text-overflow: ellipsis;">
                {card_html_content}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <style>
        .note-topic-container {
            margin-top: 5px;
            display: flex;
            align-items: center;
        }
        .note-topic-input {
            flex: 1;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown('<div class="note-topic-container">', unsafe_allow_html=True)
    note_topic = st.text_input("输入主题词以参照人设生成笔记", key=f"note_topic_{idx}")
    if st.button("开始生成", key=f"generate_{idx}"):
        with st.spinner("正在生成笔记..."):
            notes = ""
            streamed_response = st.empty()  # 创建占位符用于显示流式响应

            for content_chunk in generate_notes_stream(description, note_topic):
                notes += content_chunk
                streamed_response.markdown(
                    f"""
                    <div style='background-color: #FFFFFF; padding: 10px; border-radius: 10px; margin: 5px 0;'>
                        <strong>生成中:</strong> {notes}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                time.sleep(0.06)  # 模拟生成延迟

            st.session_state.notes[idx] = notes
            st.rerun()

    if st.session_state.notes[idx]:
        st.write(st.session_state.notes[idx])

