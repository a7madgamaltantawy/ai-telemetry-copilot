from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.services.data_loader import load_telemetry_data
from backend.services.anomaly_detection import detect_anomalies
from backend.services.langchain_chain import build_prompt
from backend.services.llm_service import generate_summary

router = APIRouter()


class CopilotRequest(BaseModel):
    question: str


@router.post("/")
def ask_copilot(payload: CopilotRequest):
    try:
        # Load data
        df = load_telemetry_data()

        # Run anomaly detection
        scored = detect_anomalies(df)

        # Basic stats
        total_records = len(scored)
        anomaly_count = int(scored["anomaly_flag"].sum())
        anomaly_percentage = (
            round((anomaly_count / total_records) * 100, 2)
            if total_records > 0
            else 0.0
        )

        # Sensor averages (safe)
        avg_sensor_1 = round(float(scored["sensor_1"].mean()), 2)
        avg_sensor_2 = round(float(scored["sensor_2"].mean()), 2)
        avg_sensor_3 = round(float(scored["sensor_3"].mean()), 2)

        # Get anomaly rows
        anomaly_rows = scored[scored["anomaly_flag"] == 1].head(5)

        # Dynamically select existing columns
        columns_to_show = []
        for col in ["timestamp", "engine_id", "sensor_1", "sensor_2", "sensor_3"]:
            if col in anomaly_rows.columns:
                columns_to_show.append(col)

        # Build anomaly sample safely
        if not anomaly_rows.empty and columns_to_show:
            sample_anomalies = anomaly_rows[columns_to_show].to_string(index=False)
        else:
            sample_anomalies = "No anomalous rows or matching columns found."

        # Build prompt
        prompt = build_prompt(
            question=payload.question,
            total_records=total_records,
            anomaly_count=anomaly_count,
            anomaly_percentage=anomaly_percentage,
            avg_sensor_1=avg_sensor_1,
            avg_sensor_2=avg_sensor_2,
            avg_sensor_3=avg_sensor_3,
            sample_anomalies=sample_anomalies,
        )

        # Generate AI response (mock or real)
        answer = generate_summary(prompt)

        return {
            "answer": answer,
            "summary_stats": {
                "total_records": total_records,
                "anomaly_count": anomaly_count,
                "anomaly_percentage": anomaly_percentage,
                "avg_sensor_1": avg_sensor_1,
                "avg_sensor_2": avg_sensor_2,
                "avg_sensor_3": avg_sensor_3,
            },
        }

    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))