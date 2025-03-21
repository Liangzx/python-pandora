import os
from langchain_deepseek import ChatDeepSeek
from dotenv import load_dotenv

# # Load the API key from .env file
load_dotenv()
api_key = os.getenv("DEEPSEEK_KEY", None)
print(api_key)

# # 初始化 DeepSeek 聊天模型
# llm = ChatDeepSeek(api_key=api_key)
# llm.invoke()
data = b"hello"
print(len(data))
