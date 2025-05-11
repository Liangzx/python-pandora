# https://python.langchain.com/api_reference/core/runnables/langchain_core.runnables.base.Runnable.html

from langchain_core.runnables import RunnableLambda

# A RunnableSequence constructed using the `|` operator
sequence = RunnableLambda(lambda x: x + 1) | RunnableLambda(lambda x: x * 2)
print(sequence.invoke(1)) # 4
print(sequence.batch([1, 2, 3])) # [4, 6, 8]

# A sequence that contains a RunnableParallel constructed using a dict literal
sequence = RunnableLambda(lambda x: x + 1) | {
    'mul_2': RunnableLambda(lambda x: x * 2),
    'mul_5': RunnableLambda(lambda x: x * 5)
}
print(sequence.invoke(1)) # {'mul_2': 4, 'mul_5': 10}
