from langchain_core.prompts import PromptTemplate
from langchain_core.prompts import FewShotPromptTemplate
from langchain_chroma import Chroma
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_openai import OpenAIEmbeddings
# from langchain_deepseek import DeepSeekEmbeddings
from deepseek import DeepSeekClient
from dotenv import load_dotenv

# # Load the API key from .env file
load_dotenv()

# 自定义 DeepSeek 嵌入类
class DeepSeekEmbeddings:
    def __init__(self, api_key: str):
        self.client = DeepSeekClient(api_key=api_key)

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        """将一组文本转换为嵌入向量"""
        return self.client.get_embeddings(texts)

    def embed_query(self, text: str) -> list[float]:
        """将单个文本转换为嵌入向量"""
        return self.client.get_embeddings([text])[0]


example_prompt = PromptTemplate.from_template("Question: {question}\n{answer}")

examples = [
    {
        "question": "Who lived longer, Muhammad Ali or Alan Turing?",
        "answer": """
Are follow up questions needed here: Yes.
Follow up: How old was Muhammad Ali when he died?
Intermediate answer: Muhammad Ali was 74 years old when he died.
Follow up: How old was Alan Turing when he died?
Intermediate answer: Alan Turing was 41 years old when he died.
So the final answer is: Muhammad Ali
""",
    },
    {
        "question": "When was the founder of craigslist born?",
        "answer": """
Are follow up questions needed here: Yes.
Follow up: Who was the founder of craigslist?
Intermediate answer: Craigslist was founded by Craig Newmark.
Follow up: When was Craig Newmark born?
Intermediate answer: Craig Newmark was born on December 6, 1952.
So the final answer is: December 6, 1952
""",
    },
    {
        "question": "Who was the maternal grandfather of George Washington?",
        "answer": """
Are follow up questions needed here: Yes.
Follow up: Who was the mother of George Washington?
Intermediate answer: The mother of George Washington was Mary Ball Washington.
Follow up: Who was the father of Mary Ball Washington?
Intermediate answer: The father of Mary Ball Washington was Joseph Ball.
So the final answer is: Joseph Ball
""",
    },
    {
        "question": "Are both the directors of Jaws and Casino Royale from the same country?",
        "answer": """
Are follow up questions needed here: Yes.
Follow up: Who is the director of Jaws?
Intermediate Answer: The director of Jaws is Steven Spielberg.
Follow up: Where is Steven Spielberg from?
Intermediate Answer: The United States.
Follow up: Who is the director of Casino Royale?
Intermediate Answer: The director of Casino Royale is Martin Campbell.
Follow up: Where is Martin Campbell from?
Intermediate Answer: New Zealand.
So the final answer is: No
""",
    },
]

# 初始化 DeepSeek 嵌入模型
embeddings = DeepSeekEmbeddings(api_key="DEEPSEEK_KEY")

example_selector = SemanticSimilarityExampleSelector.from_examples(
    # This is the list of examples available to select from.
    examples,
    # This is the embedding class used to produce embeddings which are used to measure semantic similarity.
    OpenAIEmbeddings(),
    # This is the VectorStore class that is used to store the embeddings and do a similarity search over.
    Chroma,
    # This is the number of examples to produce.
    k=1,
)

# Select the most similar example to the input.
question = "Who was the father of Mary Ball Washington?"
selected_examples = example_selector.select_examples({"question": question})
print(f"Examples most similar to the input: {question}")
for example in selected_examples:
    print("\n")
    for k, v in example.items():
        print(f"{k}: {v}")

prompt = FewShotPromptTemplate(
    example_selector=example_selector,
    examples=examples,
    example_prompt=example_prompt,
    suffix="Question: {input}",
    input_variables=["input"],
)

print(
    prompt.invoke({"input": "Who was the father of Mary Ball Washington?"}).to_string()
)
