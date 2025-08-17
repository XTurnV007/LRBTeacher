from duckduckgo_search import DDGS
from config.config import bing_api_key
import requests

def internet_search(query):
    """尝试 DuckDuckGo 搜索，失败则切换到 Bing 搜索 API"""
    ddgs = DDGS()

    # 先尝试使用 DuckDuckGo 搜索
    try:
        if bing_api_key:
            print("使用Bing 搜索...")
            url = "https://api.bing.microsoft.com/v7.0/search"
            headers = {"Ocp-Apim-Subscription-Key": bing_api_key}
            params = {"q": query, "textDecorations": True, "textFormat": "HTML"}

            try:
                # 使用 Bing API 进行搜索
                response = requests.get(url, headers=headers, params=params)
                response.raise_for_status()  # 如果请求失败，抛出异常
                search_results = response.json()

                results = []
                for result in search_results.get('webPages', {}).get('value', []):
                    results.append(f"标题: {result['name']}\n链接: {result['url']}\n描述: {result['snippet']}\n")

                print(results)
                
                return '\n'.join(results) if results else "未找到相关结果。"
            except requests.exceptions.RequestException as e:
                print(f"Bing 搜索失败: {e}")
                return "Bing 搜索请求失败，请稍后再试。"
    except Exception as e:
        results = ddgs.text(query, max_results=5)
        search_results = []
        for result in results:
            search_results.append(f"标题: {result['title']}\n链接: {result['href']}\n描述: {result['body']}\n")
        return '\n'.join(search_results) if search_results else "未找到相关结果。"

    return "搜索请求失败，请稍后再试。"
