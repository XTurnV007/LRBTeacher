"""
测试国际化功能
用于调试翻译问题
"""
import streamlit as st
from utils.i18n import init_i18n, t, get_language, set_language, TRANSLATIONS

def main():
    st.title("🔍 国际化功能测试")
    
    # 初始化国际化
    init_i18n()
    
    # 显示当前语言状态
    current_lang = get_language()
    st.write(f"当前语言 / Current Language: {current_lang}")
    st.write(f"Session State Language: {st.session_state.get('language', 'Not Set')}")
    
    # 语言切换按钮
    col1, col2 = st.columns(2)
    with col1:
        if st.button("切换到中文"):
            set_language('zh')
    with col2:
        if st.button("Switch to English"):
            set_language('en')
    
    st.markdown("---")
    
    # 测试各种翻译
    st.subheader("翻译测试 / Translation Test")
    
    test_keys = [
        'app_title',
        'select_function', 
        'teaching_mode',
        'knowledge_base_management',
        'simulate_teaching',
        'interactive_teaching',
        'exercise_teaching',
        'knowledge_summary',
        'assessment_teaching'
    ]
    
    for key in test_keys:
        translation = t(key)
        st.write(f"**{key}**: {translation}")
    
    st.markdown("---")
    
    # 显示完整的翻译字典
    st.subheader("完整翻译字典 / Complete Translation Dictionary")
    
    if st.checkbox("显示翻译字典"):
        st.json(TRANSLATIONS)
    
    # 手动测试翻译
    st.subheader("手动测试 / Manual Test")
    test_key = st.text_input("输入翻译键 / Enter translation key:", "app_title")
    if test_key:
        result = t(test_key)
        st.write(f"翻译结果 / Translation result: **{result}**")

if __name__ == "__main__":
    main()