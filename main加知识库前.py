import streamlit as st
from methods.simulate_teaching import simulate_teaching_method
from methods.interactive_teaching import interactive_teaching_method
from methods.exercise_teaching import exercise_teaching_method
from methods.knowledge_summary import knowledge_summary_method
from methods.assessment_teaching import assessment_teaching_method

# 设置页面配置
st.set_page_config(
    page_title="LRBTeacher",  # 设置浏览器标签标题
    page_icon="📚",  # 设置浏览器标签图标，可以是路径、URL或emoji
    layout="wide",  # 设置页面布局为宽屏模式
    initial_sidebar_state="expanded"  # 设置侧边栏初始状态为展开
)

def main():
    st.sidebar.title("选择教学方法")
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
    
    st.markdown("""
    <style>
    .css-1aumxhk {
        background: #f0f0f0;
        border-radius: 10px;
        padding: 10px;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

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

if __name__ == "__main__":
    main()
