"""
新的API调用方式示例
基于官方最新示例进行优化
"""

from utils.api_client import create_chat_completion, create_image_generation

def example_chat_completion():
    """聊天完成示例"""
    messages = [
        {"role": "user", "content": "作为一名营销专家，请为我的产品创作一个吸引人的口号"},
        {"role": "assistant", "content": "当然，要创作一个吸引人的口号，请告诉我一些关于您产品的信息"},
        {"role": "user", "content": "智谱AI开放平台"}
    ]
    
    # 使用统一的API调用
    response = create_chat_completion(
        messages=messages,
        stream=True,
        temperature=0.7,
        max_tokens=4096
    )
    
    # 处理流式响应
    from utils.stream_handler import process_stream_response
    
    def print_callback(content):
        print(content, end='')
    
    full_response = process_stream_response(response, callback=print_callback)
    
    return full_response

def example_image_generation():
    """图像生成示例"""
    response = create_image_generation(
        prompt="一个城市在水晶瓶中欢快生活的场景，水彩画风格，展现出微观与珠宝般的美丽。"
    )
    
    return response.data[0].url

def example_non_stream_chat():
    """非流式聊天示例"""
    messages = [
        {"role": "system", "content": "你是一名小红书内容创作专家"},
        {"role": "user", "content": "请帮我写一个关于护肤的小红书笔记"}
    ]
    
    response = create_chat_completion(
        messages=messages,
        stream=False,  # 关闭流式输出
        temperature=0.8
    )
    
    return response.choices[0].message.content

if __name__ == "__main__":
    print("=== 流式聊天示例 ===")
    example_chat_completion()
    
    print("\n\n=== 非流式聊天示例 ===")
    result = example_non_stream_chat()
    print(result)
    
    print("\n\n=== 图像生成示例 ===")
    image_url = example_image_generation()
    print(f"生成的图像URL: {image_url}")