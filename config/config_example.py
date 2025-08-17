"""
配置文件示例
请不要直接修改此文件，而是在应用的配置面板中设置API密钥
"""

# API密钥配置 - 请在应用中的配置面板设置
openai_api_key = ""  # 请在配置面板中设置您的智谱AI API密钥
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

# 获取API密钥的说明
"""
智谱AI API密钥获取：
1. 访问 https://open.bigmodel.cn/
2. 注册并登录账户
3. 在控制台中创建API密钥

注意：Bing搜索功能已内置API密钥，无需额外配置
"""