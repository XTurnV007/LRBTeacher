import streamlit as st
from zhipuai import ZhipuAI
from config.config import DEFAULT_MODEL
from utils.context_manager import add_to_chat_history
from utils.api_client import get_api_client
import random
import time

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

topic_points = [    
    """***美妆与护肤***
    化妆品推荐与评测
    护肤步骤与产品推荐
    化妆技巧与教程
    皮肤问题解决方案""",

    """***时尚与穿搭***
    日常穿搭灵感
    各类风格的服饰搭配
    时尚单品推荐
    季节性穿搭指南""",

    """***美食与烹饪***
    食谱分享与烹饪教程
    餐厅推荐与美食探店
    健康饮食与营养搭配
    各地特色美食介绍""",

    """***旅行与探店***
    旅行攻略与目的地推荐
    酒店与民宿评测
    本地探店与特色小店推荐
    旅行摄影与打卡地点""",

    """***健身与运动***
    健身计划与打卡
    健身器材与装备推荐
    运动技巧与教程
    健康饮食与营养补充""",

    """***家居与生活***
    家居装饰与设计灵感
    收纳与整理技巧
    生活小窍门与DIY
    家电与家具推荐""",

    """***母婴与亲子***
    孕期知识与经验分享
    婴幼儿用品推荐
    亲子活动与教育
    育儿经验与心得""",

    """***科技与数码***
    数码产品评测与推荐
    科技新品发布与体验
    手机、电脑等电子设备使用技巧
    智能家居与科技生活""",

    """***文化与娱乐***
    书籍、电影、电视剧推荐
    音乐与艺术分享
    娱乐八卦与明星动态
    文化活动与展览推荐""",

    """***宠物与动物***
    宠物养护与训练
    宠物用品推荐
    宠物健康与医疗
    宠物日常分享与互动"""
]

def fetch_response_from_api_stream(user_input, chat_history):
    # 只发送最近的6条历史记录到API，不直接修改全局聊天记录
    if len(chat_history) > 1:
        # 排除系统消息，获取最近的6条非系统消息
        relevant_history = chat_history[1:]
        last_messages = relevant_history[-6:]
    else:
        # 只有系统消息，这是第一次对话
        last_messages = chat_history

    # 构造发送给API的消息
    messages = last_messages + [{'role': 'user', 'content': user_input}]
    
    # 调用API
    client = get_api_client()
    response = client.chat.completions.create(
        model=DEFAULT_MODEL,
        messages=messages,
        stream=True  # 开启流式响应
    )

    # 实时处理API响应
    full_response = ""
    for chunk in response:
        if chunk == "[DONE]":
            break
        if hasattr(chunk, 'choices') and chunk.choices:
            delta = chunk.choices[0].delta
            if delta and hasattr(delta, 'content') and delta.content:
                content = delta.content
                full_response += content
                yield content  # 实时返回生成的内容

    # 返回完整的响应
    return full_response



def render_chat_bubble(chat, role):
    if role == 'user':
        st.markdown(
            f"""
            <div style='background-color: #DCF8C6; padding: 10px; border-radius: 10px; margin: 5px 0; text-align: right;'>
                <strong>你:</strong> {chat}
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"""
            <div style='background-color: #FFFFFF; padding: 10px; border-radius: 10px; margin: 5px 0; border: 1px solid #E6E6E6;'>
                <strong>导师:</strong> {chat}
            </div>
            """,
            unsafe_allow_html=True
        )

# 更新聊天记录，限制条数为 3
def update_chat_history(chat_history, role, content):
    # 更新本地历史记录，不依赖 `st.session_state`
    chat_history.append({'role': role, 'content': content})
    if len(chat_history) > 6:
        chat_history.pop(0)  # 移除最早的一条消息
    return chat_history


def interactive_teaching_method():
    st.title("互动式教学方法")

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
    st.markdown('<p class="description">方法简介：通过角色扮演和故事演绎的方式，用户分析导师（大语言模型）给的小红书角色和背景故事，思考并回答导师的提问。</p>', unsafe_allow_html=True)
    
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
        st.session_state.started = False

    if not st.session_state.started:
        if st.button("开始"):
            st.session_state.started = True
            # 初始化聊天记录，包含系统消息
            st.session_state.chat_history = [
                {'role': 'system', 'content': "同学你好~我将为你创建角色和背景故事，认真阅读下面的内容哦~"}
            ]
            st.rerun()

    if st.session_state.started:
        # 用容器管理聊天记录和用户输入
        chat_container = st.container()
        input_container = st.container()

        with chat_container:
            # 渲染聊天记录
            for chat in st.session_state.chat_history:
                render_chat_bubble(chat["content"], chat["role"])

            # 初始角色生成逻辑（仅在聊天记录中只有系统消息时触发）
            if len(st.session_state.chat_history) == 1:  # 系统消息已初始化
                with st.spinner("正在生成初始回复..."):
                    random_note = random.choice(knowledge_points)
                    random_topic = random.choice(topic_points)
                    initial_prompt = f'''根据主题{random_topic},为用户拟定一个小红书角色和生动有趣的背景故事（包括背景、内容方向、目标受众以及营销策略），并根据角色，需要提出一个易于回答的且与小红书内容创作相关的问题。从以下内容中选题：{random_note}；'''
                    chat_generator = fetch_response_from_api_stream(initial_prompt, st.session_state.chat_history)
                    response_content = ""
                    streamed_response = st.empty()  # 用于显示流式内容

                    for chunk in chat_generator:
                        response_content += chunk
                        streamed_response.markdown(
                            f"""
                            <div style='background-color: #FFFFFF; padding: 10px; border-radius: 10px; margin: 5px 0; border: 1px solid #E6E6E6;'>
                                <strong>导师:</strong> {response_content}
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                        time.sleep(0.06)  # 模拟流式响应效果

                    # 将完整响应加入聊天记录
                    st.session_state.chat_history.append({
                        'role': 'assistant',
                        'content': response_content
                    })
                    st.rerun()  # 刷新页面以显示完整聊天记录

        with input_container:
            # 检查输入框状态键是否存在
            if "user_input_state" not in st.session_state:
                st.session_state.user_input_state = ""

            # 使用 `value` 绑定到 `st.session_state.user_input_state`，而不是直接修改 `st.session_state.user_input`
            user_input = st.text_area(
                "请输入你的回答:",
                value=st.session_state.user_input_state,
                key="user_input",  # 保留组件唯一键
                placeholder="请输入内容..."
            )

            # 同步输入框的内容到辅助状态变量
            st.session_state.user_input_state = user_input

            if st.button("发送", key="send_button"):
                if user_input.strip():
                    # 将用户输入添加到聊天记录
                    st.session_state.chat_history.append({"role": "user", "content": user_input})
                    # 清空输入框状态
                    st.session_state.user_input_state = ""
                    st.rerun()  # 刷新页面显示聊天记录并清空输入框


        # 针对多轮交互的优化逻辑
        if st.session_state.chat_history and st.session_state.chat_history[-1]["role"] == "user":
            user_input = st.session_state.chat_history[-1]["content"]
            with chat_container:
                with st.spinner("正在生成回复..."):
                    # 动态情绪价值反馈
                    positive_feedback = (
                        f""
                    )

                    # 构造后续互动引导的 prompt
                    follow_up_prompt = (
                        "根据以下背景故事和用户回答，与用户互动并补充用户回答的不足，同时进一步拓展问题，引导用户深入思考：\n"
                        f"背景故事：{st.session_state.chat_history[1]['content']}\n"
                        "对话历史：\n" +
                        "\n".join([f"{chat['role']}: {chat['content']}" for chat in st.session_state.chat_history]) +
                        f"\n用户最新回答：{user_input}\n"
                        "请注意问题应具有启发性，并保持积极支持的语气。"
                    )

                    # 调用 API 流式生成响应
                    chat_generator = fetch_response_from_api_stream(follow_up_prompt, st.session_state.chat_history[:-1])
                    response_content = positive_feedback  # 初始化为情绪价值反馈内容
                    streamed_response = st.empty()  # 创建占位符显示流式响应

                    for chunk in chat_generator:
                        response_content += chunk
                        streamed_response.markdown(
                            f"""
                            <div style='background-color: #FFFFFF; padding: 10px; border-radius: 10px; margin: 5px 0; border: 1px solid #E6E6E6;'>
                                <strong>导师:</strong> {response_content}
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                        time.sleep(0.06)  # 模拟流式延迟效果

                    # 将完整回复加入聊天记录
                    st.session_state.chat_history.append({"role": 'assistant', "content": response_content})
                    st.rerun()  # 刷新页面以显示完整聊天记录


