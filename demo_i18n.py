"""
国际化功能演示
运行此文件来测试中英文界面切换
"""
import streamlit as st
from utils.i18n import init_i18n, t, language_selector

def main():
    # 初始化国际化
    init_i18n()
    
    # 设置页面配置
    st.set_page_config(
        page_title=t('app_title'),
        page_icon="🌐",
        layout="wide"
    )
    
    st.title("🌐 " + t('app_title') + " - 国际化演示")
    
    # 显示语言选择器
    language_selector()
    
    st.markdown("---")
    
    # 演示各种翻译
    st.header("界面元素演示")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("教学功能")
        st.write(f"• {t('simulate_teaching')}")
        st.write(f"• {t('interactive_teaching')}")
        st.write(f"• {t('exercise_teaching')}")
        st.write(f"• {t('knowledge_summary')}")
        st.write(f"• {t('assessment_teaching')}")
        st.write(f"• {t('knowledge_base_management')}")
        
    with col2:
        st.subheader("配置管理")
        st.write(f"• {t('api_key_management')}")
        st.write(f"• {t('zhipu_ai')} API")
        st.write(f"• {t('model_configuration')}")
        st.write(f"• {t('save_configuration')}")
        st.write(f"• {t('language')} {t('settings')}")
    
    st.markdown("---")
    
    # 交互演示
    st.header("交互演示")
    
    if st.button(t('start')):
        st.success(f"✅ {t('success')}!")
        st.balloons()
    
    user_input = st.text_input(t('enter_answer'), placeholder=t('enter_content_placeholder'))
    
    if st.button(t('send')) and user_input:
        st.info(f"{t('you')}: {user_input}")
        st.info(f"{t('tutor')}: {t('generating_reply')}...")
    
    st.markdown("---")
    
    # 显示当前语言信息
    current_lang = st.session_state.get('language', 'zh')
    lang_name = t('chinese') if current_lang == 'zh' else t('english')
    st.info(f"当前语言 / Current Language: {lang_name} ({current_lang})")
    
    st.markdown("---")
    st.markdown(f"**{t('copyright')}**")
    st.markdown(f"*{t('powered_by')}*")

if __name__ == "__main__":
    main()