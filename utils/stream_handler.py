"""
统一的流式响应处理工具
"""

def process_stream_response(response, callback=None):
    """
    处理流式响应
    
    Args:
        response: API响应对象
        callback: 可选的回调函数，用于实时处理每个chunk
    
    Returns:
        完整的响应文本
    """
    result = ""
    
    try:
        for chunk in response:
            if chunk == "[DONE]":
                break
                
            # 检查chunk是否有有效内容
            if (hasattr(chunk, 'choices') and 
                chunk.choices and 
                hasattr(chunk.choices[0], 'delta') and
                chunk.choices[0].delta and
                hasattr(chunk.choices[0].delta, 'content') and
                chunk.choices[0].delta.content):
                
                content = chunk.choices[0].delta.content
                result += content
                
                # 如果有回调函数，调用它
                if callback:
                    callback(content)
                    
    except Exception as e:
        print(f"Error processing stream response: {e}")
        
    return result

def process_stream_response_generator(response):
    """
    生成器版本的流式响应处理
    
    Args:
        response: API响应对象
    
    Yields:
        每个chunk的内容
    """
    try:
        for chunk in response:
            if chunk == "[DONE]":
                break
                
            # 检查chunk是否有有效内容
            if (hasattr(chunk, 'choices') and 
                chunk.choices and 
                hasattr(chunk.choices[0], 'delta') and
                chunk.choices[0].delta and
                hasattr(chunk.choices[0].delta, 'content') and
                chunk.choices[0].delta.content):
                
                content = chunk.choices[0].delta.content
                yield content
                
    except Exception as e:
        print(f"Error processing stream response: {e}")

def safe_get_delta_content(chunk):
    """
    安全地获取chunk中的delta content
    
    Args:
        chunk: API响应的chunk
    
    Returns:
        content字符串或None
    """
    try:
        if (hasattr(chunk, 'choices') and 
            chunk.choices and 
            hasattr(chunk.choices[0], 'delta') and
            chunk.choices[0].delta and
            hasattr(chunk.choices[0].delta, 'content')):
            
            return chunk.choices[0].delta.content
            
    except (AttributeError, IndexError):
        pass
        
    return None