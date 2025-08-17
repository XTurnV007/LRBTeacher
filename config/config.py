# API密钥配置 - 请在应用中的配置面板设置
openai_api_key = ""  # 请在配置面板中设置您的API密钥
MAX_HISTORY_LENGTH = 5

# Bing搜索API密钥 - 使用默认密钥
bing_api_key = "e4fdd0d9bd944b858b09c9b4639c1d16"

# 模型配置
DEFAULT_MODEL = "glm-4.5"  # 默认使用的模型
# DEFAULT_MODEL = "GLM-4-Plus"  # 默认使用的模型
IMAGE_MODEL = "cogview-4-250304"  # 图像生成模型

# 模型调用参数配置
MODEL_PARAMS = {
    "max_tokens": 4096,      # 最大输出tokens
    "temperature": 0.7,      # 控制输出的随机性 (0-1)
    "stream": True,          # 启用流式输出
}

# 是否启用深度思考模式（仅支持部分模型）
ENABLE_THINKING = False 
