# LangChain LangSmith 使用指南

## 1. 安装与配置
```shell
# 1. 首先安装 LangChain 和 LangSmith 客户端
pip install langchain langsmith
# 2. 设置环境变量（需要从 LangSmith 网站获取 API 密钥）
export LANGCHAIN_TRACING_V2=true
export LANGCHAIN_API_KEY=<your-api-key>
export LANGCHAIN_PROJECT=<your-project-name>  # 可选，默认为"default"

```

## 2. 基本功能

跟踪链和代理的运行

```python
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_openai import OpenAI

prompt = PromptTemplate.from_template("Tell me a joke about {topic}")
chain = LLMChain(llm=OpenAI(), prompt=prompt)
chain.run(topic="programmers")  # 这将被记录到 LangSmith
```
查看跟踪记录
登录 LangSmith 网站
导航到你的项目
查看最近的运行记录，包括输入、输出和中间步骤

## 3. 高级功能

测试数据集
创建数据集：

在 LangSmith 界面中手动创建

或以编程方式上传：

```python
from langsmith import Client

client = Client()
dataset_name = "Joke Examples"
dataset = client.create_dataset(dataset_name)
client.create_examples(
    dataset_id=dataset.id,
    inputs=[{"topic": "programmers"}, {"topic": "cats"}],
    outputs=["Why do programmers...", "Why did the cat..."])
```
运行评估：

```python
from langsmith.evaluation import evaluate

evaluate(
    "joke-evaluation",
    data=dataset_name,
    llm_or_chain_factory=lambda: chain,
    evaluation=evaluators,  # 自定义或使用预设评估器
)
```

自定义评估
```python
from langsmith.schemas import Example, Run

def exact_match(run: Run, example: Example) -> dict:
    return {"score": run.outputs["output"] == example.outputs}

evaluate(
    "exact-match-eval",
    data=dataset_name,
    llm_or_chain_factory=lambda: chain,
    evaluation=exact_match,
)
```

4. 监控生产环境
在生产中启用跟踪
```python

from langchain.callbacks.manager import tracing_v2_enabled

with tracing_v2_enabled(project_name="prod-joke-generator"):
    chain.run(topic="programmers")
```
设置警报
在 LangSmith 界面中，可以：

设置性能指标阈值

配置异常检测

设置 Slack 或电子邮件通知

5. 最佳实践
项目组织：为不同环境（开发、测试、生产）创建不同项目

数据集版本控制：定期更新测试数据集以反映真实使用情况

评估指标：结合自动评估和人工评估

监控：设置关键性能指标的仪表板和警报

LangSmith 提供了强大的工具来改进和监控你的 LangChain 应用程序，从开发到生产部署的全生命周期管理。

https://docs.smith.langchain.com/
