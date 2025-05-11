import httpx
from pydantic import BaseModel, Field
from openai import OpenAI
import os
from langchain_deepseek import ChatDeepSeek
from dotenv import load_dotenv
from langchain_core.output_parsers import PydanticToolsParser
from langchain.callbacks.tracers import LangChainTracer
# https://python.langchain.com/docs/how_to/debugging/
from langchain.globals import set_verbose
from langchain.globals import set_debug

class add(BaseModel):
    """Add two integers."""

    a: int = Field(..., description="First integer")
    b: int = Field(..., description="Second integer")

# 自定义拦截器
class ToolCaptureClient(httpx.Client):
    async def post(self, url, **kwargs):
        print(">>> 请求体（Request Body）:\n", kwargs.get("json"))  # 打印请求体
        response = super().post(url, **kwargs)
        print("<<< 响应体（Response Body）:\n", response.json())  # 打印响应体
        return response

# set_debug(True)
# Load the API key from .env file
load_dotenv()
api_key = os.getenv("DEEPSEEK_KEY", None)
print(api_key)
tools = [add]
# 替换 OpenAI 的默认客户端
custom_client = ToolCaptureClient()
openai_client = OpenAI(http_client=custom_client)
llm = ChatDeepSeek(model="deepseek-chat",api_key=api_key, base_url="https://api.deepseek.com")
llm_with_tools = llm.bind_tools(tools)
llm.invoke("计算3*12")
