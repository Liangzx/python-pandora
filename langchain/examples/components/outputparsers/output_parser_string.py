from langchain_core.tools import tool
import os
from langchain_deepseek import ChatDeepSeek
from dotenv import load_dotenv
from langchain_core.output_parsers import JsonOutputParser
# https://python.langchain.com/docs/how_to/debugging/
from langchain.globals import set_verbose
from langchain.globals import set_debug
from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import StrOutputParser

@tool
def get_weather(location: str) -> str:
    """Get the weather from a location."""

    return "Sunny."

# set_debug(True)
# set_verbose(True)
# Load the API key from .env file
load_dotenv()
api_key = os.getenv("DEEPSEEK_KEY", None)
print(api_key)
tools = [get_weather]
# 初始化 DeepSeek 聊天模型
llm = ChatDeepSeek(model="deepseek-chat", verbose=True, api_key=api_key, temperature=0.0, base_url="https://api.deepseek.com")
llm_with_tools = llm.bind_tools(tools=tools)
query = "What is the weather in Beijing?"
messages = [HumanMessage(query)]
ai_msg = llm_with_tools.invoke(messages)
print(ai_msg.tool_calls)
messages.append(ai_msg)
for tool_call in ai_msg.tool_calls:
    selected_tool = {"get_weather": get_weather}[tool_call["name"].lower()]
    tool_msg = selected_tool.invoke(tool_call)
    messages.append(tool_msg)

chain = llm_with_tools | StrOutputParser()
print(chain.invoke(messages))
