from langchain.prompts import PromptTemplate

summary_prompt = PromptTemplate.from_template(
    """
You are an engineering telemetry assistant.
The user asked: {question}

Telemetry anomaly count: {anomaly_count}

Write a short engineering-style summary of the situation.
"""
)

def build_prompt(question: str, anomaly_count: int) -> str:
    return summary_prompt.format(question=question, anomaly_count=anomaly_count)