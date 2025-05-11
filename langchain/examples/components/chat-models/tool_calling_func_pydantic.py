from pydantic import BaseModel, Field
import os
from langchain.callbacks import StdOutCallbackHandler
from langchain_deepseek import ChatDeepSeek
from dotenv import load_dotenv
from langchain_core.output_parsers import PydanticToolsParser
from langchain.callbacks.tracers import LangChainTracer
# https://python.langchain.com/docs/how_to/debugging/
from langchain.globals import set_verbose
from langchain.globals import set_debug
from langchain_core.messages import HumanMessage

class add(BaseModel):
    """Add two integers."""

    a: int = Field(..., description="First integer")
    b: int = Field(..., description="Second integer")


class multiply(BaseModel):
    """Multiply two integers."""

    a: int = Field(..., description="First integer")
    b: int = Field(..., description="Second integer")

set_debug(True)
set_verbose(True)
# Load the API key from .env file
load_dotenv()
api_key = os.getenv("DEEPSEEK_KEY", None)
print(api_key)
tools = [add, multiply]
# 初始化 DeepSeek 聊天模型
llm = ChatDeepSeek(model="deepseek-chat", verbose=True, api_key=api_key, temperature=0.0, base_url="https://api.deepseek.com")
llm_with_tools = llm.bind_tools(tools=tools)
query = "What is 3 乘以 12?"


print("--------------")
chain = llm_with_tools | PydanticToolsParser(tools=[add, multiply])
print(chain.invoke(query))
