import os
from langchain_deepseek import ChatDeepSeek
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import AIMessagePromptTemplate
from langchain_core.prompts import HumanMessagePromptTemplate
from langchain.prompts import PromptTemplate

# # Load the API key from .env file
load_dotenv()
api_key = os.getenv("DEEPSEEK_KEY", None)
print(api_key)

# 初始化 DeepSeek 聊天模型
model = ChatDeepSeek( model="deepseek-chat",api_key=api_key, base_url="https://api.deepseek.com")

examples = [
    {"input": "2 🦜 2", "output": "4"},
    {"input": "2 🦜 3", "output": "5"},
]

# human template
human_template = "{input}"
human_prompt = PromptTemplate(
    input_variables=["input"],
    template=human_template
)
human_message_prompt = HumanMessagePromptTemplate(prompt=human_prompt)

# ai template
ai_template = "{output}"
ai_prompt = PromptTemplate(
    input_variables=["output"],
    template=ai_template
)
ai_message_prompt = AIMessagePromptTemplate(prompt=ai_prompt)
example_prompt = ChatPromptTemplate(
    [
        human_message_prompt,
        ai_message_prompt,
    ]
)
few_shot_prompt = FewShotChatMessagePromptTemplate(
    example_prompt=example_prompt,
    examples=examples,
)


final_prompt = ChatPromptTemplate(
    [
        ("system", "You are a wondrous wizard of math."),
        few_shot_prompt,
        ("human", "{input}"),
    ]
)

chain = final_prompt | model
print(chain.invoke({"input": "What's 2 🦜 9?"}))
