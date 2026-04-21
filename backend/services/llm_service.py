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


def _extract_question(text: str) -> str:
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if line.strip().lower() == "the user question:" and i + 1 < len(lines):
            return lines[i + 1].strip()
    return ""


def _mock_engineering_summary(prompt: str) -> str:
    question = _extract_question(prompt).lower()

    total_records = _extract_numeric_value(prompt, "Total records:")
    anomaly_count = _extract_numeric_value(prompt, "Total anomalies:")
    anomaly_percentage = _extract_numeric_value(prompt, "Anomaly percentage:")
    avg_sensor_1 = _extract_numeric_value(prompt, "Average sensor_1:")
    avg_sensor_2 = _extract_numeric_value(prompt, "Average sensor_2:")
    avg_sensor_3 = _extract_numeric_value(prompt, "Average sensor_3:")

    base = (
        f"The telemetry dataset contains {int(total_records)} records, with "
        f"{int(anomaly_count)} anomalous records (~{anomaly_percentage:.2f}%). "
    )

    if "percentage" in question or "rate" in question:
        return (
            base
            + f"The anomaly rate is approximately {anomaly_percentage:.2f}%, "
              "which indicates a limited but meaningful subset of records deviates from the dominant pattern."
        )

    if "sensor" in question or "average" in question or "trend" in question:
        return (
            base
            + f"Average operating values are sensor_1={avg_sensor_1:.2f}, "
              f"sensor_2={avg_sensor_2:.2f}, and sensor_3={avg_sensor_3:.2f}. "
              "These values suggest a stable overall baseline, with anomalies concentrated in a subset of samples."
        )

    if "review" in question or "engineering" in question:
        return (
            base
            + f"From an engineering review perspective, the average values remain around "
              f"sensor_1={avg_sensor_1:.2f}, sensor_2={avg_sensor_2:.2f}, and sensor_3={avg_sensor_3:.2f}. "
              "The flagged anomalies should be investigated further, but no root-cause claim should be made without additional context."
        )

    if "anomal" in question or "abnormal" in question:
        return (
            base
            + "The anomaly detection results indicate that most records follow the dominant operating pattern, "
              "while a smaller subset shows abnormal behavior requiring focused inspection."
        )

    return (
        base
        + f"Average values remain near sensor_1={avg_sensor_1:.2f}, "
          f"sensor_2={avg_sensor_2:.2f}, and sensor_3={avg_sensor_3:.2f}. "
          "Overall, the results suggest stable bulk behavior with a distinct anomalous subset."
    )


def generate_summary(prompt: str) -> str:
    if not USE_LLM or not client:
        return _mock_engineering_summary(prompt)

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an engineering telemetry assistant. "
                        "Write concise, technically grounded summaries of anomaly behavior."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
        )
        return response.choices[0].message.content or "No response returned."
    except Exception as exc:
        return f"LLM error: {str(exc)}"