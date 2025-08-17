# API 调用迁移指南

## 概述

根据智谱AI官方最新示例，我们对项目中的API调用方式进行了优化和统一。

## 主要改进

### 1. 统一的API调用客户端

创建了 `utils/api_client.py` 文件，提供统一的API调用接口：

- `create_chat_completion()` - 聊天完成API
- `create_image_generation()` - 图像生成API

### 2. 新增配置参数

在 `config/config.py` 中新增了以下配置：

```python
# 模型调用参数配置
MODEL_PARAMS = {
    "max_tokens": 4096,      # 最大输出tokens
    "temperature": 0.7,      # 控制输出的随机性 (0-1)
    "stream": True,          # 启用流式输出
}

# 是否启用深度思考模式（仅支持部分模型）
ENABLE_THINKING = False
```

### 3. 改进的流式响应处理

优化了流式响应的处理方式，更符合官方示例：

```python
# 旧方式
for chunk in response:
    if chunk == "[DONE]":
        break
    if hasattr(chunk, 'choices') and chunk.choices:
        delta = chunk.choices[0].delta
        if delta and hasattr(delta, 'content'):
            content = delta.content

# 新方式
for chunk in response:
    if chunk.choices[0].delta.content:
        content = chunk.choices[0].delta.content
```

## 使用示例

### 基本聊天完成

```python
from utils.api_client import create_chat_completion

messages = [
    {"role": "user", "content": "你好"}
]

response = create_chat_completion(
    messages=messages,
    stream=True,
    temperature=0.7
)

# 处理流式响应
for chunk in response:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end='')
```

### 图像生成

```python
from utils.api_client import create_image_generation

response = create_image_generation(
    prompt="一个美丽的风景"
)

image_url = response.data[0].url
```

### 深度思考模式

如需启用深度思考模式，在 `config/config.py` 中设置：

```python
ENABLE_THINKING = True
```

注意：深度思考模式仅支持 `glm-4.5` 和 `glm-4-plus` 模型。

## 迁移步骤

1. **更新导入语句**：
   ```python
   # 旧方式
   from zhipuai import ZhipuAI
   from config.config import openai_api_key, DEFAULT_MODEL
   client = ZhipuAI(api_key=openai_api_key)
   
   # 新方式
   from utils.api_client import create_chat_completion
   ```

2. **更新API调用**：
   ```python
   # 旧方式
   response = client.chat.completions.create(
       model=DEFAULT_MODEL,
       messages=messages,
       stream=True
   )
   
   # 新方式
   response = create_chat_completion(
       messages=messages,
       stream=True
   )
   ```

3. **更新流式响应处理**：
   ```python
   # 旧方式
   for chunk in response:
       if hasattr(chunk, 'choices') and chunk.choices:
           delta = chunk.choices[0].delta
           if delta and hasattr(delta, 'content'):
               content = delta.content
   
   # 新方式
   for chunk in response:
       if chunk.choices[0].delta.content:
           content = chunk.choices[0].delta.content
   ```

## 优势

1. **统一管理**：所有API调用参数在配置文件中统一管理
2. **更好的错误处理**：统一的错误处理机制
3. **更简洁的代码**：减少重复代码，提高可维护性
4. **符合官方规范**：遵循智谱AI官方最新示例
5. **支持新特性**：支持深度思考模式等新功能

## 注意事项

1. 确保所有文件都使用新的API调用方式
2. 深度思考模式仅在支持的模型上启用
3. 流式响应处理更加严格，需要检查内容是否存在
4. 配置参数可以根据需要调整