"""
配置管理工具
提供动态修改配置的功能
"""

import streamlit as st
from config.config import DEFAULT_MODEL, IMAGE_MODEL, MODEL_PARAMS, ENABLE_THINKING

def show_config_panel():
    """显示配置面板"""
    st.sidebar.markdown("---")
    
    # API密钥管理
    st.sidebar.markdown("### 🔑 API密钥管理")
    
    # 显示配置提示
    if not st.session_state.get("openai_api_key", ""):
        st.sidebar.warning("⚠️ 请配置智谱AI API密钥以使用完整功能")
    
    # OpenAI API密钥输入
    openai_key = st.sidebar.text_input(
        "智谱AI API密钥",
        type="password",
        value=st.session_state.get("openai_api_key", ""),
        placeholder="请输入您的智谱AI API密钥",
        key="openai_key_input",
        help="用于调用GLM模型的API密钥，获取地址：https://open.bigmodel.cn/"
    )
    
    # 保存API密钥
    if st.sidebar.button("💾 保存API密钥", key="save_api_keys"):
        st.session_state.openai_api_key = openai_key
        st.sidebar.success("API密钥已保存！")
    
    # 显示API密钥状态
    openai_status = "✅" if st.session_state.get("openai_api_key", "") else "❌"
    st.sidebar.markdown(f"智谱AI: {openai_status}")
    st.sidebar.markdown("Bing搜索: ✅ (已内置)")  # 显示Bing搜索已内置
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### ⚙️ 模型配置")
    
    # 模型选择
    model_options = [
        "glm-4.5",
        "GLM-4-Plus", 
        "glm-3-turbo"
    ]
    
    current_model = st.sidebar.selectbox(
        "选择聊天模型",
        model_options,
        index=model_options.index(DEFAULT_MODEL) if DEFAULT_MODEL in model_options else 0,
        key="model_selector"
    )
    
    # 图像模型选择
    image_model_options = [
        "cogview-4-250304",
        "CogView-3-Plus"
    ]
    
    current_image_model = st.sidebar.selectbox(
        "选择图像模型",
        image_model_options,
        index=image_model_options.index(IMAGE_MODEL) if IMAGE_MODEL in image_model_options else 0,
        key="image_model_selector"
    )
    
    # 参数配置
    st.sidebar.markdown("#### 模型参数")
    
    temperature = st.sidebar.slider(
        "Temperature (随机性)",
        min_value=0.0,
        max_value=1.0,
        value=MODEL_PARAMS.get("temperature", 0.7),
        step=0.1,
        key="temperature_slider"
    )
    
    max_tokens = st.sidebar.number_input(
        "Max Tokens",
        min_value=100,
        max_value=8192,
        value=MODEL_PARAMS.get("max_tokens", 4096),
        step=100,
        key="max_tokens_input"
    )
    
    enable_stream = st.sidebar.checkbox(
        "启用流式输出",
        value=MODEL_PARAMS.get("stream", True),
        key="stream_checkbox"
    )
    
    enable_thinking = st.sidebar.checkbox(
        "启用深度思考模式",
        value=ENABLE_THINKING,
        help="仅支持 glm-4.5 和 glm-4-plus 模型",
        key="thinking_checkbox"
    )
    
    # 保存配置按钮
    if st.sidebar.button("💾 保存配置", key="save_config"):
        save_config(
            model=current_model,
            image_model=current_image_model,
            temperature=temperature,
            max_tokens=max_tokens,
            stream=enable_stream,
            thinking=enable_thinking
        )
        st.sidebar.success("配置已保存！")
        st.rerun()
    
    # 重置配置按钮
    if st.sidebar.button("🔄 重置为默认", key="reset_config"):
        reset_config()
        st.sidebar.success("已重置为默认配置！")
        st.rerun()
    
    return {
        "model": current_model,
        "image_model": current_image_model,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "stream": enable_stream,
        "thinking": enable_thinking
    }

def save_config(model, image_model, temperature, max_tokens, stream, thinking):
    """保存配置到session state"""
    st.session_state.current_config = {
        "DEFAULT_MODEL": model,
        "IMAGE_MODEL": image_model,
        "MODEL_PARAMS": {
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": stream
        },
        "ENABLE_THINKING": thinking
    }

def get_api_keys():
    """获取当前的API密钥"""
    from config.config import bing_api_key
    return {
        "openai_api_key": st.session_state.get("openai_api_key", ""),
        "bing_api_key": bing_api_key  # 使用配置文件中的默认值
    }

def is_api_configured():
    """检查API密钥是否已配置"""
    keys = get_api_keys()
    return bool(keys["openai_api_key"])  # 只检查OpenAI密钥

def reset_config():
    """重置配置"""
    if "current_config" in st.session_state:
        del st.session_state.current_config

def get_current_config():
    """获取当前配置"""
    if "current_config" in st.session_state:
        return st.session_state.current_config
    
    # 返回默认配置
    return {
        "DEFAULT_MODEL": DEFAULT_MODEL,
        "IMAGE_MODEL": IMAGE_MODEL,
        "MODEL_PARAMS": MODEL_PARAMS,
        "ENABLE_THINKING": ENABLE_THINKING
    }

def update_api_client_config():
    """更新API客户端配置"""
    config = get_current_config()
    
    # 这里可以动态更新API客户端的配置
    # 由于Python的模块导入机制，我们使用session_state来传递配置
    st.session_state.api_config = config
    
    return config