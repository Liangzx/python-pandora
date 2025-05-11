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
model = ChatDeepSeek(model="deepseek-chat",api_key=api_key, temperature=0.0, base_url="https://api.deepseek.com")

examples = [
    {"input": "2 🦜 2", "output": "4"},
    {"input": "2 🦜 3", "output": "5"},
]

# This is a prompt template used to format each individual example.
example_prompt = ChatPromptTemplate.from_messages(
    [
        ("human", "{input}"),
        ("ai", "{output}"),
    ]
)
few_shot_prompt = FewShotChatMessagePromptTemplate(
    example_prompt=example_prompt,
    examples=examples,
)

print(few_shot_prompt.invoke({}).to_messages())
print("-------------------\n")
print(few_shot_prompt.format())
print("-------------------\n")
final_prompt = ChatPromptTemplate(
    [
        ("system", "You are a wondrous wizard of math."),
        few_shot_prompt,
        ("human", "{input}"),
    ]
)

# prompt = """
# System: You are a wondrous wizard of math.
# Human: 2 🦜 2
# AI: 4
# Human: 2 🦜 3
# AI: 5
# Human: What is 2 🦜 9?
# AI:
# """
# print(model.invoke(prompt))
# print("-------------------\n")

chain = final_prompt | model
print(chain.invoke({"input": "What's 2 🦜 9?"}))
