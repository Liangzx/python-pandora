from langchain.prompts import PromptTemplate

# 多变量模板
# 定义多变量模板
template = "请写一篇关于 {topic} 的短文，字数不少于 {word_count} 字。"
prompt = PromptTemplate(
    input_variables=["topic", "word_count"],  # 定义多个变量
    template=template,
)

# 使用模板生成提示
formatted_prompt = prompt.format(topic="气候变化", word_count=500)
print(formatted_prompt)
