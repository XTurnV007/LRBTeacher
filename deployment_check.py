"""
部署检查工具
用于验证 Streamlit Community Cloud 部署状态
"""
import streamlit as st
import sys
import os
from datetime import datetime
from utils.i18n import init_i18n, t, get_language, TRANSLATIONS

st.set_page_config(
    page_title="部署检查",
    page_icon="🔍",
    layout="wide"
)

def main():
    st.title("🔍 部署状态检查")
    
    # 显示部署信息
    st.subheader("📊 系统信息")
    st.write(f"**Python 版本**: {sys.version}")
    st.write(f"**当前时间**: {datetime.now()}")
    st.write(f"**工作目录**: {os.getcwd()}")
    
    # 检查文件是否存在
    st.subheader("📁 文件检查")
    files_to_check = [
        'utils/i18n.py',
        'main.py',
        'config/config.py'
    ]
    
    for file_path in files_to_check:
        exists = os.path.exists(file_path)
        status = "✅" if exists else "❌"
        st.write(f"{status} {file_path}")
    
    # 国际化测试
    st.subheader("🌐 国际化测试")
    
    try:
        init_i18n()
        current_lang = get_language()
        st.success(f"✅ 国际化初始化成功，当前语言: {current_lang}")
        
        # 测试翻译
        test_translation = t('app_title')
        st.write(f"**测试翻译 (app_title)**: {test_translation}")
        
        # 显示可用语言
        available_langs = list(TRANSLATIONS.keys())
        st.write(f"**可用语言**: {available_langs}")
        
        # 语言切换测试
        col1, col2 = st.columns(2)
        with col1:
            if st.button("测试中文"):
                st.session_state.language = 'zh'
                st.rerun()
        with col2:
            if st.button("Test English"):
                st.session_state.language = 'en'
                st.rerun()
                
        # 显示当前翻译状态
        st.write("**当前翻译示例**:")
        sample_keys = ['teaching_mode', 'knowledge_base_management', 'simulate_teaching']
        for key in sample_keys:
            st.write(f"- {key}: {t(key)}")
            
    except Exception as e:
        st.error(f"❌ 国际化测试失败: {str(e)}")
    
    # Session State 检查
    st.subheader("🔧 Session State")
    st.json(dict(st.session_state))

if __name__ == "__main__":
    main()