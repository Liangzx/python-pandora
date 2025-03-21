from langchain.prompts import PromptTemplate

# 结合 Few-shot Prompting
# 定义 Few-shot 模板
template = """
以下是几个示例：
示例 1: {example1}
示例 2: {example2}

请根据以上示例，写一篇关于 {topic} 的短文。
"""
prompt = PromptTemplate(
    input_variables=["example1", "example2", "topic"],
    template=template,
)

# 使用模板生成提示
formatted_prompt = prompt.format(
    example1="示例 1: 人工智能正在改变世界。",
    example2="示例 2: 区块链技术具有去中心化的特点。",
    topic="量子计算"
)
print(formatted_prompt)
