import os
from langchain_deepseek import ChatDeepSeek
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# # Load the API key from .env file
load_dotenv()
api_key = os.getenv("DEEPSEEK_KEY", None)
print(api_key)
 # 初始化 DeepSeek 聊天模型
model = ChatDeepSeek(model="deepseek-chat",api_key=api_key, temperature=0.0, base_url="https://api.deepseek.com")
prompt = ChatPromptTemplate.from_template("tell me a joke about {topic}")
chain = prompt | model | StrOutputParser()
# print(chain.invoke({"topic": "bears"}))
analysis_prompt = ChatPromptTemplate.from_template("is this a funny joke? {joke}")
# The dict in the chain is automatically parsed and converted into a RunnableParallel,
# which runs all of its values in parallel and returns a dict with the results.
composed_chain = {"joke": chain} | analysis_prompt | model | StrOutputParser()
print(composed_chain.invoke({"topic": "bears"}))


# https://python.langchain.com/docs/how_to/sequence/
