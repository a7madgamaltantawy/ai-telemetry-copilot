# AI Telemetry Copilot

A telemetry monitoring platform that processes engineering sensor data, detects anomalies, and exposes results through APIs and a simple dashboard.

This project is being developed as a step toward integrating AI and LLM capabilities into engineering data systems.

---

## Current Features

- Telemetry data ingestion from processed datasets
- Anomaly detection using Isolation Forest
- FastAPI backend exposing telemetry and anomaly endpoints
- Streamlit dashboard for basic data visualization
- Modular architecture ready for AI/LLM integration

---

## Tech Stack

- Python
- FastAPI
- Pandas / NumPy
- Scikit-learn
- Streamlit

---

## Project Structure



---

## How to Run the Project

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/ai-telemetry-copilot.git
cd ai-telemetry-copilot
```

### 2. Create a virtual environment
```bash
python -m venv .venv
source .venv/bin/activate   # macOS/Linux
# .venv\Scripts\activate    # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Add sample data
Make sure you have a CSV file at:
```text
data/processed/telemetry_processed.csv
```

### 5. Run the FastAPI backend
```bash
uvicorn backend.main:app --reload
```

Open in your browser:
```text
http://127.0.0.1:8000/docs
```

### 6. Run the Streamlit dashboard
```bash
streamlit run app/streamlit_app.py
```

Then open:
```text
http://localhost:8501
```

