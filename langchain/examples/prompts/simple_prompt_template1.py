from langchain.prompts import PromptTemplate

# 基本用法
# 定义提示模板
template = "请写一篇关于 {topic} 的短文。"
prompt = PromptTemplate(
    input_variables=["topic"],  # 定义模板中的变量
    template=template,          # 定义模板内容
)

# 使用模板生成提示
formatted_prompt = prompt.format(topic="人工智能")
print(formatted_prompt)
