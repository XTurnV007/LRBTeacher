import streamlit as st
from zhipuai import ZhipuAI
from config.config import DEFAULT_MODEL
from utils.context_manager import add_to_chat_history
from utils.api_client import get_api_client
from utils.i18n import t
import re
import random

knowledge_points = [
    """***内容构思的核心原则***
    牢记内容创作的每一环节都应服务于目的，避免冗余和离题。明确你的内容是为了哪一群体服务，解决他们什么问题，然后围绕这一中心思想布局全文。
    内容定位：在动笔之前，先确定内容的受众群体和核心信息。例如，针对学生党的祛痘产品分享，需明确你的内容将如何贴近他们的实际需求和兴趣点。
    配图选择：图片是吸引用户停留的第一步。浏览小红书上的热门帖子，了解平台偏好的风格，如使用明亮、有视觉冲击力的图片或前后对比图。确保图片与内容主题紧密相连，提升整体吸引力。
    标题制作：运用公式“目标人群+用户痛点+解决方案”来构思标题，如“学生党必看！7天击退痘痘秘籍”。此外，可以尝试不同的情感触发词（如“震惊”、“亲身经历”）来增加标题的吸引力。""",
    
    """***定位和目标受众分析***
    用户画像：分析小红书的主要用户特征（如性别、年龄、兴趣、消费能力等），了解平台用户偏好。
    细分市场：明确你的内容领域，如美妆、旅行、健身、美食等。细分领域的内容更容易吸引特定用户。
    价值主张：思考如何为目标受众提供实际价值，如实用干货、个性化建议等，以增加用户的关注度。""",
    
    """***内容策划与选题***
    热门趋势：关注小红书的热门话题和标签，了解哪些内容容易爆红。可以利用平台内的“热搜榜”和“趋势榜”进行选题。
    用户需求：研究用户在特定领域中最关心的话题和痛点，制作相关内容满足需求，增强内容的吸引力。
    内容周期：根据节假日、换季等时间点，制定与之相关的内容策划，比如节假日推荐、季节护肤、美食节探店等。""",
    
    """***视觉内容创作***
    高质量的图片和视频：学习基础摄影、后期处理技巧，确保图片和视频的清晰度、美观度。小红书的用户非常注重视觉体验。
    风格一致性：保持账号的视觉风格一致，这样有助于品牌形象的建立。
    封面设计：封面是吸引用户点击的关键，可以通过添加文字说明、强调主题等方式提升封面吸引力。""",
    
    """***文案技巧***
    标题吸引力：标题要简洁有趣，直接点出内容亮点，比如“平价护肤品推荐”“适合小个子的穿搭技巧”等。
    内容丰富性：内容要尽可能详细且有条理，涵盖图片、文字、心得等，让用户阅读有收获。
    互动性：增加提问、邀请用户参与话题，增强互动性。比如，“你最喜欢哪款产品？”、“还有哪些值得推荐的地方？”""",
    
    """***数据分析和优化***
    数据跟踪：关注内容的阅读量、点赞量、评论数、转发数等，通过数据分析找出用户最喜欢的内容类型。
    迭代优化：根据数据反馈不断调整内容策略，优化内容方向。比如高互动度的内容要多发，低互动度的内容类型则可以优化或减少发布。
    时间发布规律：测试并确定内容发布时间，找出最佳的发布时间段，提高内容的曝光量。""",
    
    """***营销和推广***
    合作推广：可以与其他小红书博主或品牌合作，进行内容互推或联名活动。
    话题标签：使用热门话题标签，但避免标签堆砌，确保标签与内容的相关性，提高曝光机会。
    定期互动：定期回复评论、与粉丝互动，提升账号活跃度，同时也增加用户黏性。"""
]


def fetch_question_from_api(notes_input):
    random_note = random.choice(knowledge_points)
    prompt = f'''根据'{notes_input}',帮我为小红书博主的关键知识点生成1个带A,B,C,D四个选项的练习题，使用练习式教学方法，只需要问题。
                从以下内容中选题：{random_note}；
                一定要和'{notes_input}相关,务必生成1个带A,B,C,D四个选项的练习题！（        
                # OutputFormat :
                "question":
                "options": []）不要有多余的符号'''
    messages = [
        {'role': 'system', 'content': """
        你是一名小红书博主导师。
        # OutputFormat :
       "question":
        "options": []
        """},
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

def parse_question_response(response):
    try:
        # 清洗掉反斜杠
        response = response.replace('\\"', '')

        # 找到 question 的起始位置
        question_start = response.find('"question":') + len('"question":')
        question_end = response.find('"options":')
        question = response[question_start:question_end].strip().strip('"')

        if question.startswith("："):
            question = question[1:].strip()

        question = question.strip()

        # 找到 options 的起始位置
        options_start = response.find('[', question_end) + 1
        options_end = response.find(']', options_start)
        options_str = response[options_start:options_end].strip()

        # 分割选项并保持标点符号
        options = re.findall(r'\"(.*?)\"', options_str)
        options = [opt.strip() for opt in options]

        # 为每个选项添加前缀（A.、B.等）
        # options = [f"{chr(65+i)}. {opt}" for i, opt in enumerate(options)]

        return question, options
    except Exception as e:
        st.error(t('parse_error'))
        st.error(f"{t('error_info')} {e}")
        return None, None


def validate_answer(question, selected_option):
    prompt = f"""这是一个练习题的答案反馈，请判断用户选择的答案是否正确，并给出解释。
    问题: {question}
    用户选择的答案: {selected_option}"""
    
    messages = [
        {'role': 'system', 'content': """
        你是一名小红书博主导师。
        # OutputFormat :
        "is_correct":
        "explanation":
        """},
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

    # 提取所需部分
    try:
        is_correct_start = result.find('"is_correct":') + len('"is_correct":')
        is_correct_end = result.find(',', is_correct_start)
        is_correct = result[is_correct_start:is_correct_end].strip()

        explanation_start = result.find('"explanation":') + len('"explanation":')
        explanation_end = result.find('}', explanation_start)
        explanation = result[explanation_start:explanation_end].strip()

        # 清理提取的值
        is_correct = is_correct.replace('"', '').strip()
        explanation = explanation.replace('"', '').strip()

        return is_correct, explanation
    except Exception as e:
        st.error(t('parse_answer_error'))
        st.error(f"{t('error_info')} {e}")
        return None, None

def exercise_teaching_method():
    st.title(t('exercise_teaching'))
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
    st.markdown(f'<p class="description">{t("exercise_description")}</p>', unsafe_allow_html=True)
    notes_input = st.text_input(t('enter_practice_content'), "")
    
    if st.button(t('generate_exercise')):
        with st.spinner(t('generating_exercise')):
            response = fetch_question_from_api(notes_input)
            if response:
                question, options = parse_question_response(response)
                if question and options:
                    if 'questions' not in st.session_state:
                        st.session_state['questions'] = []
                    # 将新题目添加到题目列表的开头
                    st.session_state['questions'].insert(0, {
                        'question': question,
                        'options': options,
                        'selected_option': None,
                        'is_correct': None,
                        'explanation': None
                    })
    
    if 'questions' in st.session_state:
        total_questions = len(st.session_state['questions'])
        # 使用从1到total_questions递增的序号
        for i, q in enumerate(st.session_state['questions']):
            question_text = q['question'].strip().rstrip('",')
            question_number = total_questions - i  # 计算当前题目的序号
            st.write(f"**{t('question')} {question_number}: {question_text}**")
            selected_option = st.radio(t('select_answer', question_number), q['options'], key=f"selected_option_{question_number}")
            if selected_option != q['selected_option']:
                st.session_state['questions'][i]['selected_option'] = selected_option
            
            if st.button(t('submit_answer', question_number)):
                with st.spinner(t('verifying_answer')):
                    is_correct, explanation = validate_answer(q['question'], selected_option)
                    st.session_state['questions'][i]['is_correct'] = is_correct
                    st.session_state['questions'][i]['explanation'] = explanation
                
            # 显示答案反馈
            if q['is_correct'] is not None:
                st.write(t('answer_correct', question_number) + f": {q['is_correct']}")
                st.write(f"{t('explanation')}: {q['explanation']}")



exercise_teaching_method()
