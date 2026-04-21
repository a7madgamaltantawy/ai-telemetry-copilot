import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(page_title="AI Telemetry Copilot", layout="wide")
st.title("AI Telemetry Copilot")

csv_path = Path("data/processed/telemetry_processed.csv")

if csv_path.exists():
    df = pd.read_csv(csv_path)
    st.subheader("Telemetry sample")
    st.dataframe(df.head(50), use_container_width=True)

    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    if numeric_cols:
        selected = st.selectbox("Select sensor", numeric_cols)
        st.line_chart(df[selected])

    st.subheader("Copilot prompt ideas")
    st.write("- Which units show abnormal behavior?")
    st.write("- Summarize current anomaly trend")
    st.write("- What changed before anomalies?")
else:
    st.warning("No processed telemetry file found yet.")