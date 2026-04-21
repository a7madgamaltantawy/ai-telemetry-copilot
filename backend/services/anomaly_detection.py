import pandas as pd
from sklearn.ensemble import IsolationForest

FEATURE_COLUMNS = ["sensor_1", "sensor_2", "sensor_3"]

def detect_anomalies(df: pd.DataFrame) -> pd.DataFrame:
    missing = [c for c in FEATURE_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    result = df.copy()
    model = IsolationForest(n_estimators=100, contamination=0.05, random_state=42)
    result["anomaly_flag"] = model.fit_predict(result[FEATURE_COLUMNS])
    result["anomaly_flag"] = result["anomaly_flag"].map({1: 0, -1: 1})
    return result