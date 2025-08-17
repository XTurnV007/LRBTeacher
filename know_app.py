import streamlit as st
from zhipuai import ZhipuAI
from config.config import DEFAULT_MODEL
from utils.context_manager import add_to_chat_history
from utils.api_client import get_api_client
from utils.i18n import init_i18n, t, language_selector
from graphviz import Digraph

# 设置页面配置


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
    # 初始化国际化
    init_i18n()
    
    st.title(t('knowledge_graph_generator'))
    
    # 显示语言选择器
    language_selector()

    notes_input = st.text_area(t('enter_notes'), "", height=150)

    if st.button(t('generate_knowledge_graph')):
        with st.spinner(t('generating_knowledge_graph')):
            response = fetch_knowledge_from_api(notes_input)
            if response:
                formatted_response = format_markdown(response)
                graph = create_knowledge_graph(formatted_response)
                st.graphviz_chart(graph.source, use_container_width=True)
            else:
                st.error(t('api_response_empty'))

if __name__ == "__main__":
    main()
