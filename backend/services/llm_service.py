import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

USE_LLM = os.getenv("USE_LLM", "false").lower() == "true"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = None
if USE_LLM and OPENAI_API_KEY:
    client = OpenAI(api_key=OPENAI_API_KEY)


def _extract_numeric_value(text: str, label: str) -> float:
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("- "):
            stripped = stripped[2:].strip()

        if stripped.startswith(label):
            raw_value = stripped.replace(label, "", 1).replace("%", "").strip()
            try:
                return float(raw_value)
            except ValueError:
                return 0.0
    return 0.0


def _mock_engineering_summary(prompt: str) -> str:
    total_records = _extract_numeric_value(prompt, "Total records:")
    anomaly_count = _extract_numeric_value(prompt, "Total anomalies:")
    anomaly_percentage = _extract_numeric_value(prompt, "Anomaly percentage:")
    avg_sensor_1 = _extract_numeric_value(prompt, "Average sensor_1:")
    avg_sensor_2 = _extract_numeric_value(prompt, "Average sensor_2:")
    avg_sensor_3 = _extract_numeric_value(prompt, "Average sensor_3:")

    return (
        f"Engineering summary: {int(anomaly_count)} anomalies were detected out of "
        f"{int(total_records)} telemetry records (~{anomaly_percentage:.2f}%). "
        f"The dataset shows stable average values around sensor_1={avg_sensor_1:.2f}, "
        f"sensor_2={avg_sensor_2:.2f}, and sensor_3={avg_sensor_3:.2f}. "
        f"This indicates a limited subset of records deviates from the dominant operating pattern. "
        f"Further review should focus on the flagged anomalous samples while avoiding unsupported "
        f"root-cause conclusions without additional context."
    )


def generate_summary(prompt: str) -> str:
    if not USE_LLM or not client:
        return _mock_engineering_summary(prompt)

    try:
        response = client.responses.create(
            model="gpt-4o-mini",
            instructions=(
                "You are an engineering telemetry assistant. "
                "Write concise, technically grounded summaries of anomaly behavior."
            ),
            input=prompt,
        )
        return response.output_text or "No response returned."
    except Exception as exc:
        return f"LLM error: {str(exc)}"