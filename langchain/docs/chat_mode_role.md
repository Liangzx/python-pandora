在 AI 大模型聊天模型（如 OpenAI 的 GPT 系列）中，通常有三种主要的角色（roles），分别是 System、User（或 Human）和 Assistant（或 AI）。这些角色用于构建多轮对话，并帮助模型理解上下文和任务。

1. System（系统）
作用：系统角色用于设置对话的背景、任务或行为准则。它通常用于初始化对话，告诉模型应该如何表现。
示例：
System: You are a helpful assistant.
System: You are a math tutor. Answer questions clearly and step by step.
特点：
系统消息通常不会被用户直接看到，而是用于指导模型的行为。
系统消息可以定义模型的角色、语气或任务。

2. User（用户）
作用：用户角色代表与模型交互的人。用户的消息是模型需要回应的输入。
示例：
User: What is the capital of France?
User: Can you help me solve this math problem?
特点：
用户消息是模型生成回应的依据。
在多轮对话中，用户消息会与之前的对话历史一起作为上下文。

3. Assistant（助手）
作用：助手角色代表模型的回复。它是模型生成的输出。
示例：
Assistant: The capital of France is Paris.
Assistant: Sure! Let's solve the math problem step by step.
特点：
助手消息是模型对用户消息的回应。
在多轮对话中，助手消息会成为对话历史的一部分，影响后续的交互。

总结
System：设置模型的行为和任务。
User：代表用户的输入。
Assistant：代表模型的输出。
这些角色共同构成了多轮对话的上下文，帮助模型理解任务并生成合适的回复。
