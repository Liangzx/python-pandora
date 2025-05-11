from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
import os
from langchain_deepseek import ChatDeepSeek
from dotenv import load_dotenv


# # Load the API key from .env file
load_dotenv()
api_key = os.getenv("DEEPSEEK_KEY", None)
print(api_key)

# 初始化 DeepSeek 聊天模型
model = ChatDeepSeek(model="deepseek-chat",api_key=api_key, temperature=0.0, base_url="https://api.deepseek.com")


# Define your desired data structure.
class Joke(BaseModel):
    setup: str = Field(description="question to set up a joke")
    punchline: str = Field(description="answer to resolve the joke")

# And a query intented to prompt a language model to populate the data structure.
joke_query = "Tell me a joke."

# Set up a parser + inject instructions into the prompt template.
parser = JsonOutputParser(pydantic_object=Joke)

prompt = PromptTemplate(
    template="Answer the user query.\n{format_instructions}\n{query}\n",
    input_variables=["query"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)
print(prompt.invoke({"query": joke_query}).to_string())
# chain = prompt | model | parser

# print(chain.invoke({"query": joke_query}))

# Without Pydantic
print("-----------------Without Pydantic-----------------")
joke_query = "Tell me a joke."

parser = JsonOutputParser()

prompt = PromptTemplate(
    template="Answer the user query.\n{format_instructions}\n{query}\n",
    input_variables=["query"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)
print(prompt.invoke({"query": joke_query}).to_string())
chain = prompt | model | parser

# chain.invoke({"query": joke_query})
