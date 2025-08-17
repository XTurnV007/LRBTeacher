"""
统一的API调用客户端
"""
import streamlit as st
from zhipuai import ZhipuAI
from config.config import DEFAULT_MODEL, MODEL_PARAMS, ENABLE_THINKING

def get_api_client():
    """获取API客户端实例"""
    # 从session state获取API密钥
    api_key = st.session_state.get("openai_api_key", "")
    
    if not api_key:
        st.error("⚠️ 请在侧边栏配置面板中设置OpenAI API密钥")
        st.stop()
    
    return ZhipuAI(api_key=api_key)

def get_runtime_config():
    """获取运行时配置"""
    if "api_config" in st.session_state:
        return st.session_state.api_config
    
    # 返回默认配置
    return {
        "DEFAULT_MODEL": DEFAULT_MODEL,
        "IMAGE_MODEL": None,
        "MODEL_PARAMS": MODEL_PARAMS,
        "ENABLE_THINKING": ENABLE_THINKING
    }

def create_chat_completion(messages, model=None, stream=None, **kwargs):
    """
    统一的聊天完成API调用
    
    Args:
        messages: 消息列表
        model: 模型名称，默认使用配置中的DEFAULT_MODEL
        stream: 是否流式输出，默认使用配置中的设置
        **kwargs: 其他参数
    
    Returns:
        API响应
    """
    # 获取API客户端
    client = get_api_client()
    
    # 获取运行时配置
    config = get_runtime_config()
    current_model = model or config["DEFAULT_MODEL"]
    current_params = config["MODEL_PARAMS"]
    
    # 使用配置
    params = {
        "model": current_model,
        "messages": messages,
        "max_tokens": kwargs.get("max_tokens", current_params["max_tokens"]),
        "temperature": kwargs.get("temperature", current_params["temperature"]),
        "stream": stream if stream is not None else current_params["stream"],
    }
    
    # 如果启用深度思考模式且模型支持
    if config["ENABLE_THINKING"] and current_model.lower() in ["glm-4.5", "glm-4-plus"]:
        params["thinking"] = {"type": "enabled"}
    
    # 添加其他自定义参数
    for key, value in kwargs.items():
        if key not in ["max_tokens", "temperature"]:
            params[key] = value
    
    return client.chat.completions.create(**params)

def create_image_generation(prompt, model=None, **kwargs):
    """
    统一的图像生成API调用
    
    Args:
        prompt: 图像描述
        model: 模型名称
        **kwargs: 其他参数
    
    Returns:
        API响应
    """
    from config.config import IMAGE_MODEL
    
    # 获取API客户端
    client = get_api_client()
    
    # 获取运行时配置
    config = get_runtime_config()
    current_image_model = model or config.get("IMAGE_MODEL") or IMAGE_MODEL
    
    params = {
        "model": current_image_model,
        "prompt": prompt,
    }
    
    # 添加其他自定义参数
    params.update(kwargs)
    
    return client.images.generations(**params)