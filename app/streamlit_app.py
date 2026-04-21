import streamlit as st
import pandas as pd
from pathlib import Path
import requests

st.set_page_config(page_title="AI Telemetry Copilot", layout="wide")

st.title("AI Telemetry Copilot")
st.write("AI-enhanced telemetry monitoring for anomaly detection and engineering insights.")

csv_path = Path("data/processed/telemetry_processed.csv")

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Telemetry Data")

    if csv_path.exists():
        df = pd.read_csv(csv_path)
        st.dataframe(df.head(50), use_container_width=True)

        numeric_cols = df.select_dtypes(include="number").columns.tolist()
        if numeric_cols:
            selected = st.selectbox("Select a sensor to visualize", numeric_cols)
            st.line_chart(df[selected])
    else:
        st.warning("No processed telemetry file found yet.")

with col2:
    st.subheader("Copilot")

    question = st.text_area(
        "Ask the telemetry copilot",
        value="Summarize anomaly situation for engineering review",
        height=120,
    )

    if st.button("Generate Summary"):
        try:
            response = requests.post(
                "http://127.0.0.1:8000/copilot/",
                json={"question": question},
                timeout=30,
            )

            if response.status_code == 200:
                result = response.json()

                st.success("Summary generated")
                st.write(result["answer"])

                stats = result.get("summary_stats", {})
                if stats:
                    st.subheader("Summary Stats")
                    st.json(stats)
            else:
                st.error(f"API error: {response.status_code}")
                st.write(response.text)

        except Exception as exc:
            st.error(f"Could not connect to backend: {exc}")

st.markdown("---")
st.subheader("Suggested Questions")
st.write("- Which operating pattern appears abnormal?")
st.write("- Summarize the anomaly level for engineering review")
st.write("- What do the current telemetry statistics suggest?")