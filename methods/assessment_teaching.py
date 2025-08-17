import streamlit as st
from utils.api_client import create_chat_completion
from utils.context_manager import add_to_chat_history
from utils.i18n import t
import time
import re

def assess_content(content):
    prompt = f'''请评估以下内容，并为其打分（1到10分），指出不足之处并提供改进方向：\n\n{content}。参照以下评分标准：
            ***信息价值***
            实用性：笔记是否为用户提供了有价值的建议、解决方案或有用的信息。如果用户从中获得实际帮助，笔记的评分会更高。
            深度与专业性：内容是否具有一定的深度，尤其是针对某个领域或话题的专业性分析，能够提供独特见解的内容，会获得更好的评分。
            ***可读性和语言质量***
            语言表达清晰：笔记的文字是否流畅、简洁、清晰，逻辑是否清晰明了，避免冗长的句子或语法错误。
            排版与结构：文本的排版是否整洁，段落之间是否有清晰的分隔，使得用户阅读起来舒适。适当的分段、标题、加粗等可以提高可读性。
            ***标题的吸引力***
            简洁精准：标题要能够简洁明了地表达笔记的核心内容，吸引用户点击。避免过度夸张或与内容不符的标题。
            关键字使用：合理使用与内容相关的关键词，有助于提高文本的可见度，尤其是在平台的搜索和推荐机制中。
            ***情感表达和用户共鸣***
            情感共鸣：文本是否能引起用户的情感共鸣。分享个人经历、真实感受、富有感染力的语言能够打动读者，增加点赞、评论等互动。
            积极正面：虽然小红书允许多样化的表达方式，但总体上，积极向上的文本更容易获得用户的认可和平台的推荐。
            ***原创性和独特性***
            独特视角：文本是否能提供不同于常规视角的见解，或是从一个独特的角度分析问题。具有差异化的内容容易获得较高的评分。
            避免抄袭：平台会对重复内容和抄袭行为进行监控，文本内容的独特性能够直接影响评分。
            ***内容符合平台规定***
            确保文本内容遵守小红书平台的规则，包括避免使用低俗、恶心、误导等语言，避免宣传不合规产品或服务。违规的文本会受到惩罚，评分会降低。'''
    messages = [
        {'role': 'system', 'content': "你是一名经验丰富的老师，擅长评估（1到10分）和改进学生的写作内容。"},
        {'role': 'user', 'content': prompt}
    ]

    response = create_chat_completion(
        messages=messages,
        stream=True,
    )

    result = ""
    for chunk in response:
        if chunk == "[DONE]":
            break
        if hasattr(chunk, 'choices') and chunk.choices and chunk.choices[0].delta.content:
            content = chunk.choices[0].delta.content
            result += content
            yield content  # 实时返回生成的内容

    add_to_chat_history('assistant', result)
    return result

def extract_score(assessment_result):
    match = re.search(r"评分：(\d+)/10", assessment_result)
    if match:
        return int(match.group(1))
    return None

def display_stars(score):
    stars = "⭐" * score + "☆" * (10 - score)
    return stars

def assessment_teaching_method():
    st.title(t('assessment_teaching'))
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

    # 方法简介
    st.markdown(f'<p class="description">{t("assessment_description")}</p>', unsafe_allow_html=True)

    # 初始化 session_state 变量
    if "assessment_input" not in st.session_state:
        st.session_state.assessment_input = ""
    if "assessment_result" not in st.session_state:
        st.session_state.assessment_result = ""
    if "assessment_score" not in st.session_state:
        st.session_state.assessment_score = None
    if "new_evaluation" not in st.session_state:
        st.session_state.new_evaluation = False  # 控制是否刚完成评估

    # 使用 session_state 存储输入和结果
    content_input = st.text_area(t('write_content'), value=st.session_state.assessment_input, key="input_area")
    st.markdown("""
    <style>
        .stTextArea textarea {
            min-height: 300px;
        }
    </style>
    """, unsafe_allow_html=True)

    if st.button(t('assess_content')):
        with st.spinner(t('assessing')):
            # 调用流式评估函数
            st.session_state.new_evaluation = True  # 标记新评估完成
            assessment_result = ""
            
            # 使用列布局固定评分的位置
            col1, col2 = st.columns([3, 1])
            
            with col1:
                result_placeholder = st.empty()  # 用于显示流式响应
            
            with col2:
                score_placeholder = st.empty()   # 用于显示评分

            # 调用评估函数并实时更新结果
            for chunk in assess_content(content_input):
                assessment_result += chunk
                result_placeholder.markdown(assessment_result, unsafe_allow_html=True)
                
                # 动态更新评分
                score = extract_score(assessment_result)
                if score is not None:
                    stars = display_stars(score)
                    score_placeholder.markdown(f"**{t('score')}** {stars} ({score}/10)")
                
                time.sleep(0.06)  # 模拟流式延迟效果

            # 更新 session_state 以保存新评估结果
            st.session_state.assessment_input = content_input
            st.session_state.assessment_result = assessment_result
            st.session_state.assessment_score = extract_score(assessment_result)

    # 显示上次评估结果
    if st.session_state.assessment_result and not st.session_state.new_evaluation:
        st.write(t('last_assessment_result'))
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown(st.session_state.assessment_result, unsafe_allow_html=True)
        
        with col2:
            if st.session_state.assessment_score is not None:
                stars = display_stars(st.session_state.assessment_score)
                st.markdown(f"**{t('score')}** {stars} ({st.session_state.assessment_score}/10)")

    # 重置新评估标记
    st.session_state.new_evaluation = False


            
            # 确保最终评分更新
            # score = extract_score(assessment_result)
            # if score is not None:
            #     stars = display_stars(score)
            #     score_placeholder.markdown(f"**最终评分：** {stars} ({score}/10)")
            # st.write(assessment_result)

# Streamlit app entry point
if __name__ == "__main__":
    assessment_teaching_method()
