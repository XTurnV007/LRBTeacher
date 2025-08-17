import streamlit as st
from methods.simulate_teaching import simulate_teaching_method
from methods.interactive_teaching import interactive_teaching_method
from methods.exercise_teaching import exercise_teaching_method
from methods.knowledge_summary import knowledge_summary_method
from methods.assessment_teaching import assessment_teaching_method
from knowledge_base.knowledge_base_management import knowledge_base_management_method
from utils.css_styles import apply_css_styles
from utils.config_manager import show_config_panel, update_api_client_config
from utils.i18n import init_i18n, t, language_selector

# 设置页面配置 - 必须在其他 Streamlit 命令之前
st.set_page_config(
    page_title="LRBTeacher",  # 浏览器标签标题，无法动态翻译
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    # 初始化国际化
    init_i18n()
    
    # 强制清除所有缓存
    if hasattr(st, 'cache_data'):
        st.cache_data.clear()
    
    # 应用 CSS 样式
    apply_css_styles()
    
    # 自定义侧边栏样式
    st.markdown(
        """
        <style>
        [data-testid="stSidebar"] {
            background-color: #FF2E4D !important;
            min-width: 380px !important;
            width: 380px !important;
        }
        [data-testid="stSidebar"] > div {
            width: 380px !important;
        }
        /* 强制设置radio按钮容器宽度 */
        [data-testid="stSidebar"] .stRadio {
            width: 100% !important;
        }
        [data-testid="stSidebar"] .stRadio > div {
            width: 100% !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    # 在侧边栏中添加 Logo 和标题
    st.sidebar.markdown(
        f"""
        <div style="padding-left: 24px; display: flex; align-items: center; margin-bottom: 20px;">
            <img src="https://raw.githubusercontent.com/XTurnV007/LRBTeacher/refs/heads/master/static/LBRTeacher.svg" 
                alt="Logo" style="width: 70px; height: auto; margin-right: 20px;">
            <h1 style="color: white; margin: 0; font-size:30px; font-weight:bold;">{t('app_title')}</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

    
    st.sidebar.markdown(
        f"""
        <div style="font-weight: bold; font-size: 14px; color: white; letter-spacing: 1px; font-family: 'Microsoft YaHei', sans-serif;margin-bottom: 40px;">
            {t('app_subtitle')}
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
        t('select_function'),
        [
            t('teaching_mode'),
            t('knowledge_base_management')
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

    if section == t('teaching_mode'):
        method = st.sidebar.selectbox(
            t('select_teaching_method'),
            [
                t('simulate_teaching'),
                t('interactive_teaching'),
                t('exercise_teaching'),
                t('knowledge_summary'),
                t('assessment_teaching')
            ],
            format_func=lambda x: f"📘 {x}"  # 添加图标
        )

        if method == t('simulate_teaching'):
            simulate_teaching_method()
        elif method == t('interactive_teaching'):
            interactive_teaching_method()
        elif method == t('exercise_teaching'):
            exercise_teaching_method()
        elif method == t('knowledge_summary'):
            knowledge_summary_method()
        elif method == t('assessment_teaching'):
            assessment_teaching_method()
    elif section == t('knowledge_base_management'):
        knowledge_base_management_method()

    # 显示语言选择器
    language_selector()
    
    # 显示配置面板并更新API客户端配置
    show_config_panel()
    update_api_client_config()

    # 在侧边栏下方添加尾注
    st.sidebar.markdown(
        f"""
        <div style="position: fixed; bottom: 20px; left: 50px; font-size: 14px; color: white; text-align: center;">
            {t('copyright')} <br>
            {t('powered_by')}
        </div>
        """,
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
