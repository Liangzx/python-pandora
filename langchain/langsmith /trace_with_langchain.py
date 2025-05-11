# https://smith.langchain.com/onboarding?organizationId=b2a02c07-e81e-41b6-8689-46eb7e953491&step=1

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os
from langchain_deepseek import ChatDeepSeek
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate
from langchain_core.prompts import ChatPromptTemplate
# You can configure a LangChainTracer instance to trace a specific invocation.
from langchain.callbacks.tracers import LangChainTracer

# # Load the API key from .env file
load_dotenv()
api_key = os.getenv("DEEPSEEK_KEY", None)
print(api_key)

 # 初始化 DeepSeek 聊天模型
model = ChatDeepSeek(model="deepseek-chat",api_key=api_key, temperature=0.0, base_url="https://api.deepseek.com")

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Please respond to the user's request only based on the given context."),
    ("user", "Question: {question}\nContext: {context}")
])

tracer = LangChainTracer()
output_parser = StrOutputParser()

chain = prompt | model | output_parser
chain.invoke({"question": "Am I using a callback?", "context": "I'm using a callback"}, config={"callbacks": [tracer]})

# LangChain Python also supports a context manager for tracing a specific block of code.
from langchain_core.tracers.context import tracing_v2_enabled
with tracing_v2_enabled():
  chain.invoke({"question": "Am I using a context manager?", "context": "I'm using a context manager"})

# This will NOT be traced (assuming LANGSMITH_TRACING is not set)
chain.invoke({"question": "Am I being traced?", "context": "I'm not being traced"})


