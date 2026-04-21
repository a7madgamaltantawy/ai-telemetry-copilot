from fastapi import FastAPI
from backend.routes.health import router as health_router
from backend.routes.telemetry import router as telemetry_router
from backend.routes.anomalies import router as anomalies_router
from backend.routes.copilot import router as copilot_router

app = FastAPI(
    title="AI Telemetry Copilot",
    description="AI-enhanced telemetry monitoring platform for anomaly detection and engineering insights.",
    version="0.1.0"
)

app.include_router(health_router, prefix="/health", tags=["Health"])
app.include_router(telemetry_router, prefix="/telemetry", tags=["Telemetry"])
app.include_router(anomalies_router, prefix="/anomalies", tags=["Anomalies"])
app.include_router(copilot_router, prefix="/copilot", tags=["Copilot"])