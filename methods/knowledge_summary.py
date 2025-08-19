import streamlit as st
import networkx as nx
import plotly.graph_objects as go
from zhipuai import ZhipuAI
from config.config import DEFAULT_MODEL
from utils.context_manager import add_to_chat_history
from utils.api_client import get_api_client
from knowledge_base.knowledge_base_management import search_local_knowledge_base, get_embeddings_for_long_text
from internet_search.duckduckgo_search import internet_search
from utils.i18n import t
import math
import random

def fetch_knowledge_from_api(notes_input, knowledge_base_result, internet_search_result):
    combined_input = f"{notes_input}\n\n知识库结果:\n{knowledge_base_result}\n\n互联网搜索结果:\n{internet_search_result}"
    prompt = f'''根据以下内容生成带等级的结构化知识:\n{combined_input}。务必严格按照以下格式生成内容：
                生成带等级的结构化知识，5个一级标题，每个一级标题下2个二级标题，每个二级标题下3个子内容。'''
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

def create_knowledge_graph(formatted_response, center_node):
    graph = nx.DiGraph()
    graph.add_node(center_node, level=0)

    lines = formatted_response.split('\n')
    current_subtopic = ""
    current_subsubtopic = ""

    for line in lines:
        if line.startswith('## '):
            current_subtopic = line.strip('# ').strip()
            graph.add_node(current_subtopic, level=1)
            graph.add_edge(center_node, current_subtopic)
            current_subsubtopic = ""
        elif line.startswith('### '):
            current_subsubtopic = line.strip('# ').strip()
            graph.add_node(current_subsubtopic, level=2)
            graph.add_edge(current_subtopic, current_subsubtopic)
        elif line.startswith('#### '):
            item = line.strip('# ').strip()
            graph.add_node(item, level=3)
            graph.add_edge(current_subsubtopic, item)
        elif line.startswith('- '):
            item = line.strip('- ').strip()
            graph.add_node(item, level=4)
            if current_subsubtopic:
                graph.add_edge(current_subsubtopic, item)
            elif current_subtopic:
                graph.add_edge(current_subtopic, item)

    return graph

def polar_layout(graph, center=(0, 0), layer_gap=7):
    pos = {}
    levels = {}
    
    # 根据节点的层级进行分类
    for node, data in graph.nodes(data=True):
        level = data['level']
        if level not in levels:
            levels[level] = []
        levels[level].append(node)
    
    # 计算每层节点的角度间隔，并适当增加最小间距
    for level, nodes in levels.items():
        angle_gap = 2 * math.pi / len(nodes)  # 保证节点在每层上均匀分布
        radius = level * layer_gap  # 层的半径

        # 计算每个节点的角度坐标
        for i, node in enumerate(nodes):
            angle = i * angle_gap  # 每个节点的角度
            x = center[0] + radius * math.cos(angle)  # 节点的 x 坐标
            y = center[1] + radius * math.sin(angle)  # 节点的 y 坐标
            pos[node] = (x, y)
    
    return pos


def plot_knowledge_graph(graph):
    pos = polar_layout(graph)  # 使用极坐标布局
    edge_x = []
    edge_y = []
    for edge in graph.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=1, color='rgba(50,50,50,0.7)'),
        hoverinfo='none',
        mode='lines')

    node_x = []
    node_y = []
    node_text = []
    node_color = []
    node_size = []
    for node in graph.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_text.append(node)
        level = graph.nodes[node]['level']
        if level == 0:
            node_color.append('rgba(217,95,2,0.9)')  # 中心节点颜色
            node_size.append(40)
        elif level == 1:
            node_color.append('rgba(27,158,119,0.8)')  # 第二级节点颜色
            node_size.append(30)
        elif level == 2:
            node_color.append('rgba(117,112,179,0.8)')  # 第三级节点颜色
            node_size.append(20)
        elif level == 3:
            node_color.append('rgba(231,41,138,0.8)')  # 第四级节点颜色
            node_size.append(15)
        else:
            node_color.append('rgba(102,166,30,0.8)')  # 更低级节点颜色
            node_size.append(10)

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        text=node_text,
        textposition="top center",
        hoverinfo='text',
        marker=dict(
            size=node_size,
            color=node_color,
            line=dict(width=2, color='rgba(50,50,50,0.5)')
        ))

    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        title='<br>Knowledge Graph',
                        titlefont_size=20,
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=40, l=40, r=40, t=40),
                        annotations=[dict(
                            text="Generated by Knowledge Management System",
                            showarrow=False,
                            xref="paper", yref="paper",
                            x=0.005, y=-0.002
                        )],
                        xaxis=dict(showgrid=False, zeroline=False),
                        yaxis=dict(showgrid=False, zeroline=False),
                        plot_bgcolor='white',
                        height=860,  # 调整图表高度
                        width=800,   # 保持宽度不变
                    )
                )
    return fig

def knowledge_summary_method():
    st.title(t('knowledge_summary'))
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
    st.markdown(f'<p class="description">{t("knowledge_summary_description")}</p>', unsafe_allow_html=True)
    if "graph_data" not in st.session_state:
        st.session_state.graph_data = None

    notes_input = st.text_area(t('enter_knowledge_to_learn'))

    if st.button(t('generate_knowledge_graph')):
        with st.spinner(t('generating_knowledge_graph')):
            with st.spinner(t('retrieving_from_knowledge_base')):
                query_embedding = get_embeddings_for_long_text(notes_input)
                knowledge_base_result = search_local_knowledge_base(query_embedding)

            with st.spinner(t('searching_internet')):
                internet_search_result = internet_search(notes_input)

            combined_knowledge_base_result = '\n'.join([f"文件名: {result[0]}, 相似度: {result[1]}" for result in knowledge_base_result])
            response = fetch_knowledge_from_api(notes_input, combined_knowledge_base_result, internet_search_result)
            print(response)
            
            if response:
                formatted_response = format_markdown(response)
                graph = create_knowledge_graph(formatted_response, notes_input)
                st.session_state.graph_data = plot_knowledge_graph(graph)
            else:
                st.error(t('api_response_empty'))

    if st.session_state.graph_data:
        st.plotly_chart(st.session_state.graph_data, use_container_width=True)

