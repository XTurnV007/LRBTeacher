import streamlit as st
from methods.simulate_teaching import simulate_teaching_method
from methods.interactive_teaching import interactive_teaching_method
from methods.exercise_teaching import exercise_teaching_method
from methods.knowledge_summary import knowledge_summary_method
from methods.assessment_teaching import assessment_teaching_method
from knowledge_base.knowledge_base_management import knowledge_base_management_method
from utils.css_styles import apply_css_styles
from utils.config_manager import show_config_panel, update_api_client_config

# 设置页面配置
st.set_page_config(
    page_title="LRBTeacher",  # 设置浏览器标签标题
    page_icon="📚",  # 设置浏览器标签图标，可以是路径、URL或emoji
    layout="wide",  # 设置页面布局为宽屏模式
    initial_sidebar_state="expanded"  # 设置侧边栏初始状态为展开
)

def main():
    # 应用 CSS 样式
    apply_css_styles()
    
    # 自定义侧边栏样式
    st.markdown(
        """
        <style>
        [data-testid="stSidebar"] {
            background-color: #FF2E4D;
            min-width: 350px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    # 在侧边栏中添加 Logo 和标题
    st.sidebar.markdown(
        """
        <div style="padding-left: 24px; display: flex; align-items: center; margin-bottom: 20px;">
            <img src="https://raw.githubusercontent.com/XTurnV007/LRBTeacher/refs/heads/master/static/LBRTeacher.svg" 
                alt="Logo" style="width: 70px; height: auto; margin-right: 20px;">
            <h1 style="color: white; margin: 0; font-size:30px; font-weight:bold;">LRBTeacher</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

    
    st.sidebar.markdown(
        """
        <div style="font-weight: bold; font-size: 14px; color: white; letter-spacing: 1px; font-family: 'Microsoft YaHei', sans-serif;margin-bottom: 40px;">
            一个由大语言模型驱动的小红书内容创作教练
        </div>
        """,
        unsafe_allow_html=True
    )

    st.sidebar.markdown(
        """
        <style>
        [data-testid="stSidebar"] .css-1l02zno {  /* 修改 sidebar 中 radio 上方的间距 */
            margin-top: 40px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    section = st.sidebar.radio(
        "选择一个功能",
        [
            "教学模式",
            "知识库管理"
        ],
        format_func=lambda x: f"⚙️ {x}"  # 添加图标
    )

    st.sidebar.markdown(
        """
        <style>
        .spacer {
            margin-top: 40px;
        }
        </style>
        <div class="spacer"></div>
        """,
        unsafe_allow_html=True
    )

    if section == "教学模式":
        method = st.sidebar.selectbox(
            "请选择一种教学方法",
            [
                "模拟教学方法",
                "互动式教学方法",
                "练习式教学方法",
                "知识总结式教学方法",
                "评估式教学方法"
            ],
            format_func=lambda x: f"📘 {x}"  # 添加图标
        )



        if method == "模拟教学方法":
            simulate_teaching_method()
        elif method == "互动式教学方法":
            interactive_teaching_method()
        elif method == "练习式教学方法":
            exercise_teaching_method()
        elif method == "知识总结式教学方法":
            knowledge_summary_method()
        elif method == "评估式教学方法":
            assessment_teaching_method()
    elif section == "知识库管理":
        knowledge_base_management_method()

    # 显示配置面板并更新API客户端配置
    show_config_panel()
    update_api_client_config()

        # 在侧边栏下方添加尾注
    st.sidebar.markdown(
        """
        <div style="position: fixed; bottom: 20px; left: 50px; font-size: 14px; color: white; text-align: center;">
            © 2025 LRBTeacher. All rights reserved. <br>
            Powered by GLM
        </div>
        """,
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
