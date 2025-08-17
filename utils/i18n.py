"""
国际化支持模块
支持中文（默认）和英文界面
Version: 2.0 - 修复翻译不生效问题
"""
import streamlit as st
import json
import os

# 默认语言
DEFAULT_LANGUAGE = 'zh'

# 翻译字典
TRANSLATIONS = {
    'zh': {
        # 主界面
        'app_title': 'LRBTeacher',
        'app_subtitle': '一个由大语言模型驱动的小红书内容创作教练',
        'select_function': '选择一个功能',
        'teaching_mode': '教学模式',
        'knowledge_base_management': '知识库管理',
        'select_teaching_method': '请选择一种教学方法',
        'copyright': '© 2025 LRBTeacher. All rights reserved.',
        'powered_by': 'Powered by GLM',
        
        # 教学方法
        'simulate_teaching': '模拟教学方法',
        'interactive_teaching': '互动式教学方法',
        'exercise_teaching': '练习式教学方法',
        'knowledge_summary': '知识总结式教学方法',
        'assessment_teaching': '评估式教学方法',
        
        # 模拟教学
        'simulate_description': '方法简介：可以模拟小红书创建账号人设，并根据主题词和人设撰写小红书笔记。',
        'content_topic': '内容主题',
        'enter_content_topic': '请输入内容主题：',
        'generate_persona': '生成人设',
        'generating_persona': '正在生成人设...',
        'persona_card': '人设卡片',
        'enter_topic_for_notes': '输入主题词以参照人设生成笔记',
        'start_generate': '开始生成',
        'generating_notes': '正在生成笔记...',
        'generating': '生成中:',
        
        # 互动式教学
        'interactive_description': '方法简介：通过角色扮演和故事演绎的方式，用户分析导师（大语言模型）给的小红书角色和背景故事，思考并回答导师的提问。',
        'start': '开始',
        'enter_answer': '请输入你的回答:',
        'enter_content_placeholder': '请输入内容...',
        'send': '发送',
        'you': '你',
        'tutor': '导师',
        'generating_initial_reply': '正在生成初始回复...',
        'generating_reply': '正在生成回复...',
        
        # 练习式教学
        'exercise_description': '方法简介：可以生成主题词关于内容创作各方面的练习题，帮助用户学习内容创作知识。',
        'enter_practice_content': '请输入你想练习的内容:',
        'generate_exercise': '生成练习题',
        'generating_exercise': '正在生成练习题...',
        'question': '问题',
        'select_answer': '请选择问题 {} 的答案:',
        'submit_answer': '提交问题 {} 的答案',
        'verifying_answer': '正在验证答案...',
        'answer_correct': '问题 {} 答案是否正确:',
        'explanation': '解释:',
        'parse_error': '解析问题时出错: 无法解析响应',
        'error_info': '错误信息:',
        'parse_answer_error': '解析答案反馈时出错',
        
        # 知识图谱
        'knowledge_graph_generator': '知识图谱生成器',
        'enter_notes': '请输入你的笔记内容:',
        'generate_knowledge_graph': '生成知识图谱',
        'generating_knowledge_graph': '正在生成知识图谱...',
        'api_response_empty': 'API 响应为空，请检查 API 请求。',
        
        # 测验应用
        'xiaohongshu_exercise': '小红书博主练习题',
        'enter_notes_content': '请输入你的笔记内容:',
        'you_selected': '你选择了:',
        
        # 知识总结式教学
        'knowledge_summary_description': '方法简介：可以将用户输入主题词的相关知识（知识库+互联网搜索）总结成知识图谱。',
        'enter_knowledge_to_learn': '请输入你想要学习的知识:',
        'generating_knowledge_graph': '正在生成知识图谱...',
        'retrieving_from_knowledge_base': '正在从知识库检索信息...',
        'searching_internet': '正在进行联网搜索...',
        
        # 评估式教学
        'assessment_description': '方法简介：扮演老师给学生的作业打分，用户在这里输入自己创作的笔记，将得到评分和反馈建议。',
        'write_content': '撰写内容',
        'assess_content': '评估内容',
        'assessing': '正在评估...',
        'last_assessment_result': '上次评估结果：',
        'score': '评分：',
        'final_score': '最终评分：',
        
        # API密钥管理
        'api_key_management': 'API密钥管理',
        'configure_api_key_warning': '请配置智谱AI API密钥以使用完整功能',
        'zhipu_api_key': '智谱AI API密钥',
        'zhipu_ai': '智谱AI',
        'enter_api_key_placeholder': '请输入您的智谱AI API密钥',
        'api_key_help': '用于调用GLM模型的API密钥，获取地址：https://open.bigmodel.cn/',
        'save_api_key': '保存API密钥',
        'api_key_saved': 'API密钥已保存！',
        'bing_search_builtin': 'Bing搜索: ✅ (已内置)',
        
        # 模型配置
        'model_configuration': '模型配置',
        'select_chat_model': '选择聊天模型',
        'select_image_model': '选择图像模型',
        'model_parameters': '模型参数',
        'temperature_randomness': 'Temperature (随机性)',
        'enable_streaming': '启用流式输出',
        'enable_thinking_mode': '启用深度思考模式',
        'thinking_mode_help': '仅支持 glm-4.5 和 glm-4-plus 模型',
        'save_configuration': '保存配置',
        'configuration_saved': '配置已保存！',
        'reset_to_default': '重置为默认',
        'reset_to_default_success': '已重置为默认配置！',
        
        # 知识库管理
        'select_operation': '选择操作',
        'upload_files': '上传文件',
        'search_files': '搜索文件',
        'view_knowledge_base': '查看知识库',
        'choose_files_to_upload': '选择文件上传',
        'process_files': '处理文件',
        'processing_files': '正在处理文件...',
        'file_processed': '文件 {} 已处理。',
        'file_processing_error': '处理文件 {} 时发生错误: {}',
        'all_files_processed': '所有文件已处理并存储嵌入向量。',
        'please_upload_files': '请上传文件。',
        'enter_query_text': '输入查询文本:',
        'search': '搜索',
        'searching': '正在搜索...',
        'search_results': '搜索结果:',
        'filename': '文件名:',
        'similarity': '相似度:',
        'please_enter_query': '请输入查询文本。',
        'existing_knowledge_base': '现有知识库内容:',
        
        # 通用
        'loading': '加载中...',
        'error': '错误',
        'success': '成功',
        'cancel': '取消',
        'confirm': '确认',
        'save': '保存',
        'delete': '删除',
        'edit': '编辑',
        'add': '添加',
        'close': '关闭',
        'open': '打开',
        'settings': '设置',
        'language': '语言',
        'chinese': '中文',
        'english': 'English',
    },
    
    'en': {
        # Main interface
        'app_title': 'LRBTeacher',
        'app_subtitle': 'An AI-powered Xiaohongshu content creation coach driven by large language models',
        'select_function': 'Select a Function',
        'teaching_mode': 'Teaching Mode',
        'knowledge_base_management': 'Knowledge Base Management',
        'select_teaching_method': 'Please select a teaching method',
        'copyright': '© 2025 LRBTeacher. All rights reserved.',
        'powered_by': 'Powered by GLM',
        
        # Teaching methods
        'simulate_teaching': 'Simulation Teaching Method',
        'interactive_teaching': 'Interactive Teaching Method',
        'exercise_teaching': 'Exercise Teaching Method',
        'knowledge_summary': 'Knowledge Summary Teaching Method',
        'assessment_teaching': 'Assessment Teaching Method',
        
        # Simulation teaching
        'simulate_description': 'Method Introduction: Simulate creating Xiaohongshu account personas and write Xiaohongshu posts based on topics and personas.',
        'content_topic': 'Content Topic',
        'enter_content_topic': 'Please enter content topic:',
        'generate_persona': 'Generate Persona',
        'generating_persona': 'Generating persona...',
        'persona_card': 'Persona Card',
        'enter_topic_for_notes': 'Enter topic to generate notes based on persona',
        'start_generate': 'Start Generate',
        'generating_notes': 'Generating notes...',
        'generating': 'Generating:',
        
        # Interactive teaching
        'interactive_description': 'Method Introduction: Through role-playing and story interpretation, users analyze Xiaohongshu characters and background stories given by the tutor (large language model), think and answer the tutor\'s questions.',
        'start': 'Start',
        'enter_answer': 'Please enter your answer:',
        'enter_content_placeholder': 'Please enter content...',
        'send': 'Send',
        'you': 'You',
        'tutor': 'Tutor',
        'generating_initial_reply': 'Generating initial reply...',
        'generating_reply': 'Generating reply...',
        
        # Exercise teaching
        'exercise_description': 'Method Introduction: Generate practice questions about various aspects of content creation based on topics to help users learn content creation knowledge.',
        'enter_practice_content': 'Please enter the content you want to practice:',
        'generate_exercise': 'Generate Exercise',
        'generating_exercise': 'Generating exercise...',
        'question': 'Question',
        'select_answer': 'Please select the answer for question {}:',
        'submit_answer': 'Submit answer for question {}',
        'verifying_answer': 'Verifying answer...',
        'answer_correct': 'Is question {} answer correct:',
        'explanation': 'Explanation:',
        'parse_error': 'Error parsing question: Unable to parse response',
        'error_info': 'Error information:',
        'parse_answer_error': 'Error parsing answer feedback',
        
        # Knowledge graph
        'knowledge_graph_generator': 'Knowledge Graph Generator',
        'enter_notes': 'Please enter your notes content:',
        'generate_knowledge_graph': 'Generate Knowledge Graph',
        'generating_knowledge_graph': 'Generating knowledge graph...',
        'api_response_empty': 'API response is empty, please check API request.',
        
        # Quiz app
        'xiaohongshu_exercise': 'Xiaohongshu Blogger Exercise',
        'enter_notes_content': 'Please enter your notes content:',
        'you_selected': 'You selected:',
        
        # 知识总结式教学
        'knowledge_summary_description': 'Method Introduction: Summarize knowledge related to user input topics (knowledge base + internet search) into knowledge graphs.',
        'enter_knowledge_to_learn': 'Please enter the knowledge you want to learn:',
        'retrieving_from_knowledge_base': 'Retrieving information from knowledge base...',
        'searching_internet': 'Searching the internet...',
        
        # 评估式教学
        'assessment_description': 'Method Introduction: Act as a teacher grading student assignments. Users input their created notes here and will receive scores and feedback suggestions.',
        'write_content': 'Write Content',
        'assess_content': 'Assess Content',
        'assessing': 'Assessing...',
        'last_assessment_result': 'Last Assessment Result:',
        'score': 'Score:',
        'final_score': 'Final Score:',
        
        # API密钥管理
        'api_key_management': 'API Key Management',
        'configure_api_key_warning': 'Please configure ZhipuAI API key to use full functionality',
        'zhipu_api_key': 'ZhipuAI API Key',
        'zhipu_ai': 'ZhipuAI',
        'enter_api_key_placeholder': 'Please enter your ZhipuAI API key',
        'api_key_help': 'API key for calling GLM models, get it at: https://open.bigmodel.cn/',
        'save_api_key': 'Save API Key',
        'api_key_saved': 'API key saved!',
        'bing_search_builtin': 'Bing Search: ✅ (Built-in)',
        
        # 模型配置
        'model_configuration': 'Model Configuration',
        'select_chat_model': 'Select Chat Model',
        'select_image_model': 'Select Image Model',
        'model_parameters': 'Model Parameters',
        'temperature_randomness': 'Temperature (Randomness)',
        'enable_streaming': 'Enable Streaming Output',
        'enable_thinking_mode': 'Enable Deep Thinking Mode',
        'thinking_mode_help': 'Only supports glm-4.5 and glm-4-plus models',
        'save_configuration': 'Save Configuration',
        'configuration_saved': 'Configuration saved!',
        'reset_to_default': 'Reset to Default',
        'reset_to_default_success': 'Reset to default configuration!',
        
        # 知识库管理
        'select_operation': 'Select Operation',
        'upload_files': 'Upload Files',
        'search_files': 'Search Files',
        'view_knowledge_base': 'View Knowledge Base',
        'choose_files_to_upload': 'Choose files to upload',
        'process_files': 'Process Files',
        'processing_files': 'Processing files...',
        'file_processed': 'File {} has been processed.',
        'file_processing_error': 'Error processing file {}: {}',
        'all_files_processed': 'All files have been processed and embeddings stored.',
        'please_upload_files': 'Please upload files.',
        'enter_query_text': 'Enter query text:',
        'search': 'Search',
        'searching': 'Searching...',
        'search_results': 'Search Results:',
        'filename': 'Filename:',
        'similarity': 'Similarity:',
        'please_enter_query': 'Please enter query text.',
        'existing_knowledge_base': 'Existing Knowledge Base Content:',
        
        # Common
        'loading': 'Loading...',
        'error': 'Error',
        'success': 'Success',
        'cancel': 'Cancel',
        'confirm': 'Confirm',
        'save': 'Save',
        'delete': 'Delete',
        'edit': 'Edit',
        'add': 'Add',
        'close': 'Close',
        'open': 'Open',
        'settings': 'Settings',
        'language': 'Language',
        'chinese': '中文',
        'english': 'English',
    }
}

def get_language():
    """获取当前语言设置"""
    if 'language' not in st.session_state:
        st.session_state.language = DEFAULT_LANGUAGE
    return st.session_state.language

def set_language(lang):
    """设置语言"""
    if lang in TRANSLATIONS:
        st.session_state.language = lang
        st.rerun()

def t(key, *args):
    """
    翻译函数
    Args:
        key: 翻译键
        *args: 格式化参数
    Returns:
        翻译后的文本
    """
    lang = get_language()
    translation = TRANSLATIONS.get(lang, {}).get(key, key)
    
    # 如果有格式化参数，进行格式化
    if args:
        try:
            return translation.format(*args)
        except:
            return translation
    
    return translation

def language_selector():
    """语言选择器组件"""
    current_lang = get_language()
    
    # 在侧边栏添加语言选择
    with st.sidebar:
        st.markdown("---")
        lang_options = {
            'zh': t('chinese'),
            'en': t('english')
        }
        
        selected_lang = st.selectbox(
            t('language'),
            options=list(lang_options.keys()),
            format_func=lambda x: lang_options[x],
            index=0 if current_lang == 'zh' else 1,
            key='language_selector'
        )
        
        if selected_lang != current_lang:
            set_language(selected_lang)
            # 强制清除缓存并重新运行
            st.cache_data.clear()
            st.rerun()

def init_i18n():
    """初始化国际化"""
    if 'language' not in st.session_state:
        st.session_state.language = DEFAULT_LANGUAGE
    
    # 强制刷新翻译缓存
    if hasattr(st, 'cache_data'):
        st.cache_data.clear()