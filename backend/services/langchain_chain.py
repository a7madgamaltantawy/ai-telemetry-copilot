from langchain.prompts import PromptTemplate

summary_prompt = PromptTemplate.from_template(
    """
You are an engineering telemetry assistant.

The user question:
{question}

Telemetry summary:
- Total records: {total_records}
- Total anomalies: {anomaly_count}
- Anomaly percentage: {anomaly_percentage}%
- Average sensor_1: {avg_sensor_1}
- Average sensor_2: {avg_sensor_2}
- Average sensor_3: {avg_sensor_3}

Example anomalous records:
{sample_anomalies}

Write a short engineering-style summary that:
1. Answers the user's question
2. Explains the anomaly level
3. Mentions the overall sensor behavior
4. Avoids unsupported root-cause claims
"""
)

def build_prompt(
    question: str,
    total_records: int,
    anomaly_count: int,
    anomaly_percentage: float,
    avg_sensor_1: float,
    avg_sensor_2: float,
    avg_sensor_3: float,
    sample_anomalies: str,
) -> str:
    return summary_prompt.format(
        question=question,
        total_records=total_records,
        anomaly_count=anomaly_count,
        anomaly_percentage=anomaly_percentage,
        avg_sensor_1=avg_sensor_1,
        avg_sensor_2=avg_sensor_2,
        avg_sensor_3=avg_sensor_3,
        sample_anomalies=sample_anomalies,
    )