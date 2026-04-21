from fastapi import APIRouter, HTTPException
from backend.services.data_loader import load_telemetry_data
from backend.services.anomaly_detection import detect_anomalies

router = APIRouter()

@router.get("/")
def get_anomalies(limit: int = 50):
    try:
        df = load_telemetry_data()
        scored = detect_anomalies(df)
        anomalies = scored[scored["anomaly_flag"] == 1]
        return {"rows": anomalies.head(limit).to_dict(orient="records")}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))