import streamlit as st
from zhipuai import ZhipuAI
from config.config import DEFAULT_MODEL
from utils.context_manager import add_to_chat_history
from utils.api_client import get_api_client
from graphviz import Digraph

def fetch_knowledge_from_api(notes_input):
    prompt = f"根据'{notes_input}',帮我生成一段结构化知识。"
    messages = [
        {'role': 'system', 'content': "你是一名知识管理专家，擅长以markdown格式生成知识框架。"},
        {'role': 'user', 'content': prompt}
    ]

    client = get_api_client()
    response = client.chat.completions.create(
        model=DEFAULT_MODEL,
        messages=messages,
        stream=True,
    )

    result = ""
    for chunk in response:
        if hasattr(chunk.choices[0], 'delta') and chunk.choices[0].delta.content:
            result += chunk.choices[0].delta.content

    add_to_chat_history('assistant', result)
    return result

def format_markdown(response):
    lines = response.split('\n')
    formatted_lines = []
    for line in lines:
        line = line.strip()
        if line:
            formatted_lines.append(line)
    return '\n'.join(formatted_lines)

def create_knowledge_graph(formatted_response):
    graph = Digraph(graph_attr={'size': '10,10', 'rankdir': 'LR', 'bgcolor': 'white'})  # 调整大小和布局方向

    lines = formatted_response.split('\n')
    current_topic = ""
    current_subtopic = ""
    current_subsubtopic = ""

    for line in lines:
        if line.startswith('## '):
            current_topic = line.strip('# ').strip()
            graph.node(current_topic, shape='box', style='filled', color='skyblue', fontname='Helvetica', fontsize='14', fontcolor='black')
            current_subtopic = ""
            current_subsubtopic = ""
        elif line.startswith('### '):
            current_subtopic = line.strip('# ').strip()
            graph.node(current_subtopic, shape='ellipse', style='filled', color='lightgrey', fontname='Helvetica', fontsize='12', fontcolor='black')
            graph.edge(current_topic, current_subtopic, color='grey', style='dashed')
            current_subsubtopic = ""
        elif line.startswith('#### '):
            current_subsubtopic = line.strip('# ').strip()
            graph.node(current_subsubtopic, shape='ellipse', style='filled', color='lightgrey', fontname='Helvetica', fontsize='10', fontcolor='black')
            graph.edge(current_subtopic, current_subsubtopic, color='grey', style='dotted')
        elif line.startswith('- '):
            item = line.strip('- ').strip()
            if current_subsubtopic:
                graph.node(item, shape='ellipse', style='filled', color='white', fontname='Helvetica', fontsize='10', fontcolor='black', penwidth='2')
                graph.edge(current_subsubtopic, item, color='grey', style='dotted')
            elif current_subtopic:
                graph.node(item, shape='ellipse', style='filled', color='white', fontname='Helvetica', fontsize='10', fontcolor='black', penwidth='2')
                graph.edge(current_subtopic, item, color='grey', style='dotted')
            else:
                graph.node(item, shape='ellipse', style='filled', color='white', fontname='Helvetica', fontsize='10', fontcolor='black', penwidth='2')
                graph.edge(current_topic, item, color='grey', style='dotted')
    
    return graph

def main():
    st.title("知识图谱生成器")

    notes_input = st.text_area("请输入你的笔记内容:", "", height=150)

    if st.button("生成知识图谱"):
        with st.spinner("正在生成知识图谱..."):
            response = fetch_knowledge_from_api(notes_input)
            if response:
                formatted_response = format_markdown(response)
                graph = create_knowledge_graph(formatted_response)
                st.graphviz_chart(graph.source, use_container_width=True)
            else:
                st.error("API 响应为空，请检查 API 请求。")

if __name__ == "__main__":
    main()
