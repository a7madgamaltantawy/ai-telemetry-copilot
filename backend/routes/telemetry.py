from fastapi import APIRouter, HTTPException
from backend.services.data_loader import load_telemetry_data

router = APIRouter()

@router.get("/")
def get_telemetry(limit: int = 50):
    try:
        df = load_telemetry_data()
        return {"rows": df.head(limit).to_dict(orient="records")}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))