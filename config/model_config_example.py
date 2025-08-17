# 模型配置使用示例

from config.config import DEFAULT_MODEL, IMAGE_MODEL

# 现在你可以通过修改 config.py 中的 DEFAULT_MODEL 来统一切换所有方法使用的模型

print(f"当前默认模型: {DEFAULT_MODEL}")
print(f"当前图像模型: {IMAGE_MODEL}")

# 如果你想切换模型，只需要修改 config.py 中的配置即可：
# DEFAULT_MODEL = "GLM-4-Plus"  # 或者其他模型如 "glm-3-turbo", "glm-4.5" 等
# IMAGE_MODEL = "cogview-4-250304"  # 或者其他图像模型

# 所有的方法文件都会自动使用新的模型配置，无需逐个修改