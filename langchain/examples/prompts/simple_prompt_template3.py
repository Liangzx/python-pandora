from langchain.prompts import PromptTemplate

# 定义带默认值的模板
template = "请写一篇关于 {topic} 的短文，字数不少于 {word_count} 字。"
prompt = PromptTemplate(
    input_variables=["topic", "word_count"],
    template=template,
    partial_variables={"word_count": "300"}  # 设置默认值
)

# 使用模板生成提示（只提供 topic）
formatted_prompt = prompt.format(topic="区块链")
print(formatted_prompt)

# 提供 word_count
formatted_prompt = prompt.format(topic="区块链", word_count=1000)
print(formatted_prompt)
