from zhipuai import ZhipuAI
from config.config import IMAGE_MODEL
from utils.api_client import get_api_client

client = get_api_client()  # 使用统一的API客户端
response = client.images.generations(
   model=IMAGE_MODEL, #填写需要调用的模型名称
   prompt=" 一个城市在水晶瓶中欢快生活的场景，水彩画风格，展现出微观与珠宝般的美丽。")
print(response.data[0].url)