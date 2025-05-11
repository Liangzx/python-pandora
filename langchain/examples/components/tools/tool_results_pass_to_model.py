from langchain_core.tools import tool
import os
from langchain_deepseek import ChatDeepSeek
from dotenv import load_dotenv
from langchain_core.output_parsers import JsonOutputParser
# https://python.langchain.com/docs/how_to/debugging/
from langchain.globals import set_verbose
from langchain.globals import set_debug
from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import PydanticOutputParser

@tool
def add(a: int, b: int) -> int:
    """Adds a and b."""
    return a + b


@tool
def multiply(a: int, b: int) -> int:
    """Multiplies a and b."""
    return a * b

# set_debug(True)
# set_verbose(True)
# Load the API key from .env file
load_dotenv()
api_key = os.getenv("DEEPSEEK_KEY", None)
print(api_key)
tools = [add, multiply]
# 初始化 DeepSeek 聊天模型
llm = ChatDeepSeek(model="deepseek-chat", verbose=True, api_key=api_key, temperature=0.0, base_url="https://api.deepseek.com")
llm_with_tools = llm.bind_tools(tools=tools)
query = "What is 3 * 12?"
messages = [HumanMessage(query)]
ai_msg = llm_with_tools.invoke(messages)
print(ai_msg.tool_calls)
messages.append(ai_msg)
for tool_call in ai_msg.tool_calls:
    selected_tool = {"add": add, "multiply": multiply}[tool_call["name"].lower()]
    tool_msg = selected_tool.invoke(tool_call)
    messages.append(tool_msg)

# print(messages)
parser = JsonOutputParser()
chain = llm_with_tools
print(chain.invoke(messages))

# https://python.langchain.com/docs/how_to/tool_results_pass_to_model/
