from pathlib import Path
import pandas as pd

DATA_PATH = Path("data/processed/telemetry_processed.csv")

def load_telemetry_data() -> pd.DataFrame:
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Missing file: {DATA_PATH}")
    return pd.read_csv(DATA_PATH)