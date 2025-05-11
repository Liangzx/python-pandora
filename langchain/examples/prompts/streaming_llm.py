import os
from langchain_deepseek import ChatDeepSeek
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate
from langchain_core.prompts import ChatPromptTemplate

# # Load the API key from .env file
load_dotenv()
api_key = os.getenv("DEEPSEEK_KEY", None)
print(api_key)

 # 初始化 DeepSeek 聊天模型
llm = ChatDeepSeek(model="deepseek-chat",api_key=api_key, temperature=0.0, base_url="https://api.deepseek.com")
for chunk in llm.stream("hello."):
    print(chunk, end="|", flush=True)
