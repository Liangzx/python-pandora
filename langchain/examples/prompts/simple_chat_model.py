import os
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

# 设置 OpenAI API 密钥
os.environ["OPENAI_API_KEY"] = "your-openai-api-key"

# 创建问答模板
prompt_template = PromptTemplate(
    input_variables=["question"],
    template="回答以下问题: {question}"
)

# 初始化 LLM 和 LLMChain
llm = OpenAI(temperature=0.7)
qa_chain = LLMChain(llm=llm, prompt=prompt_template)

# 提出问题并获取答案
question = "什么是人工智能？"
response = qa_chain.run(question)
print(response)
