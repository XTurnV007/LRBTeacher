# LRBTeacher API 调用优化总结

## 🎯 优化目标

根据智谱AI官方最新示例，对项目进行了全面的API调用优化，实现了：
- 统一的模型配置管理
- 更规范的API调用方式
- 动态配置切换功能
- 支持最新的模型特性

## 📋 主要改进

### 1. 统一配置管理 (`config/config.py`)

```python
# 模型配置
DEFAULT_MODEL = "glm-4.5"  # 默认使用的模型
IMAGE_MODEL = "cogview-4-250304"  # 图像生成模型

# 模型调用参数配置
MODEL_PARAMS = {
    "max_tokens": 4096,      # 最大输出tokens
    "temperature": 0.7,      # 控制输出的随机性 (0-1)
    "stream": True,          # 启用流式输出
}

# 是否启用深度思考模式（仅支持部分模型）
ENABLE_THINKING = False
```

### 2. 统一API客户端 (`utils/api_client.py`)

- `create_chat_completion()` - 统一的聊天完成API调用
- `create_image_generation()` - 统一的图像生成API调用
- 支持运行时配置动态切换
- 自动处理深度思考模式

### 3. 动态配置管理 (`utils/config_manager.py`)

- 侧边栏配置面板
- 实时切换模型和参数
- 配置保存和重置功能
- 可视化参数调整

### 4. 改进的流式响应处理

```python
# 优化前
for chunk in response:
    if chunk == "[DONE]":
        break
    if hasattr(chunk, 'choices') and chunk.choices:
        delta = chunk.choices[0].delta
        if delta and hasattr(delta, 'content'):
            content = delta.content

# 优化后
for chunk in response:
    if chunk.choices[0].delta.content:
        content = chunk.choices[0].delta.content
```

## 🔧 已更新的文件

### 核心文件
- `config/config.py` - 新增模型参数配置
- `utils/api_client.py` - 统一API调用客户端
- `utils/config_manager.py` - 配置管理工具
- `main.py` - 集成配置面板

### 方法文件
- `methods/assessment_teaching.py` - 评估式教学
- `methods/simulate_teaching.py` - 模拟教学
- `methods/interactive_teaching.py` - 互动式教学
- `methods/exercise_teaching.py` - 练习式教学
- `methods/knowledge_summary.py` - 知识总结
- `utils/chat_helpers.py` - 聊天辅助工具

### 其他应用文件
- `know_app.py` - 知识应用
- `quiz_app.py` - 测验应用
- `know_app copy.py` - 知识应用副本
- `draw.py` - 绘图功能

## 🚀 新功能特性

### 1. 动态模型切换
在侧边栏可以实时切换：
- 聊天模型 (glm-4.5, GLM-4-Plus, glm-3-turbo)
- 图像模型 (cogview-4-250304, CogView-3-Plus)

### 2. 参数实时调整
- Temperature (0.0-1.0)
- Max Tokens (100-8192)
- 流式输出开关
- 深度思考模式开关

### 3. 深度思考模式
- 支持 glm-4.5 和 glm-4-plus 模型
- 提供更深入的推理能力
- 可通过配置面板一键启用

### 4. 配置持久化
- 配置保存到 session state
- 支持重置为默认配置
- 实时生效，无需重启

## 📖 使用指南

### 基本使用

1. **启动应用**：
   ```bash
   streamlit run main.py
   ```

2. **配置模型**：
   - 在侧边栏找到"⚙️ 模型配置"面板
   - 选择所需的模型和参数
   - 点击"💾 保存配置"

3. **使用功能**：
   - 所有教学方法会自动使用新配置
   - 实时生效，无需重启应用

### 高级配置

1. **启用深度思考模式**：
   - 选择支持的模型 (glm-4.5 或 glm-4-plus)
   - 勾选"启用深度思考模式"
   - 保存配置

2. **调整生成参数**：
   - Temperature: 控制输出随机性
   - Max Tokens: 控制输出长度
   - 流式输出: 控制响应方式

## 🔍 技术细节

### API调用示例

```python
from utils.api_client import create_chat_completion

# 基本调用
response = create_chat_completion(
    messages=[{"role": "user", "content": "你好"}],
    stream=True
)

# 自定义参数
response = create_chat_completion(
    messages=messages,
    temperature=0.8,
    max_tokens=2048,
    stream=False
)
```

### 配置获取

```python
from utils.config_manager import get_current_config

config = get_current_config()
current_model = config["DEFAULT_MODEL"]
```

## 🎉 优势总结

1. **统一管理**：所有模型配置集中管理，易于维护
2. **动态切换**：无需修改代码即可切换模型和参数
3. **用户友好**：可视化配置界面，操作简单
4. **符合规范**：遵循智谱AI官方最新示例
5. **功能完整**：支持所有新特性，包括深度思考模式
6. **向后兼容**：保持原有功能不变，只是优化了实现方式

## 🔮 未来扩展

- 支持更多模型类型
- 添加配置导入/导出功能
- 支持多用户配置管理
- 添加性能监控和统计
- 集成更多智谱AI新功能