import streamlit as st
from zhipuai import ZhipuAI
from config.config import DEFAULT_MODEL
from utils.context_manager import add_to_chat_history
from utils.api_client import get_api_client
from utils.i18n import init_i18n, t, language_selector
import re

def fetch_question_from_api(notes_input):
    prompt = f"根据'{notes_input}',帮我为小红书博主的关键知识点生成1个带选项的练习题，使用练习式教学方法，只需要问题。"

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
    # Custom parsing logic for the API response
    try:
        # Extract question
        question_start = response.find("问题:") + len("问题:")
        question_end = response.find("A.")
        question = response[question_start:question_end].strip()

        # Remove leading colon if present
        if question.startswith("："):
            question = question[1:].strip()

        # Remove all symbols except question mark
        question = re.sub(r'[^\w\s？]', '', question)

        # Extract options
        options_str = response[question_end:].strip()
        options = options_str.split(' ')
        options = [opt.strip() for opt in options_str.split(' ') if opt]

        option_labels = ['A.', 'B.', 'C.', 'D.']
        formatted_options = []

        for label in option_labels:
            start = options_str.find(label)
            end = options_str.find(option_labels[option_labels.index(label) + 1]) if option_labels.index(label) + 1 < len(option_labels) else len(options_str)
            formatted_options.append(options_str[start:end].strip())

        # Remove duplicate letters in options
        formatted_options = [opt[2:].strip() if opt.startswith(tuple(option_labels)) else opt for opt in formatted_options]

        return question, formatted_options
    except Exception as e:
        st.error(t('parse_error'))
        st.error(f"{t('error_info')} {e}")
        return None, None

def main():
    # 初始化国际化
    init_i18n()
    
    st.title(t('xiaohongshu_exercise'))
    
    # 显示语言选择器
    language_selector()

    # 用户输入
    notes_input = st.text_input(t('enter_notes_content'), "")

    if st.button(t('generate_exercise')):
        with st.spinner(t('generating_exercise')):
            response = fetch_question_from_api(notes_input)
            if response:
                question, options = parse_question_response(response)

                if question and options:
                    # 显示题目
                    st.write(question)

                    # 显示选项按钮
                    for index, option in enumerate(options, 1):
                        if st.button(f"{chr(64 + index)}. {option}"):
                            st.write(f"{t('you_selected')}: {chr(64 + index)}")
            else:
                st.error(t('api_response_empty'))

if __name__ == "__main__":
    main()
