from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from dotenv import load_dotenv
from langchain.globals import set_debug
from pydantic import BaseModel, Field
import os
from langchain_deepseek import ChatDeepSeek
from dotenv import load_dotenv
from langchain_core.output_parsers import PydanticToolsParser
from langchain.callbacks.tracers import LangChainTracer

# 定义工具（使用 LangChain 装饰器）
@tool
def get_current_weather(location: str) -> str:
    """获取指定城市的当前天气"""
    return f"{location}的天气是25°C，晴。"

set_debug(True)
# Load the API key from .env file
load_dotenv()
api_key = os.getenv("DEEPSEEK_KEY", None)
print(api_key)
# 初始化模型并绑定工具
llm = ChatDeepSeek(model="deepseek-chat",api_key=api_key, temperature=0.0, base_url="https://api.deepseek.com")
llm_with_tools = llm.bind_tools([get_current_weather])

# 调用模型
response = llm_with_tools.invoke("上海今天天气如何？")
print(response)  # 输出工具调用请求
