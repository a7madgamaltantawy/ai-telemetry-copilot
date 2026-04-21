from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.services.data_loader import load_telemetry_data
from backend.services.anomaly_detection import detect_anomalies
from backend.services.langchain_chain import build_prompt
from backend.services.azure_openai_service import generate_summary

router = APIRouter()

class CopilotRequest(BaseModel):
    question: str

@router.post("/")
def ask_copilot(payload: CopilotRequest):
    try:
        df = load_telemetry_data()
        scored = detect_anomalies(df)
        anomaly_count = int(scored["anomaly_flag"].sum())
        prompt = build_prompt(payload.question, anomaly_count)
        answer = generate_summary(prompt, anomaly_count)
        return {"answer": answer}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))