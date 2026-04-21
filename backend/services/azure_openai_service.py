import os
from dotenv import load_dotenv

load_dotenv()

def use_azure_openai() -> bool:
    return os.getenv("USE_AZURE_OPENAI", "false").lower() == "true"

def generate_summary(question: str, anomaly_count: int) -> str:
    if not use_azure_openai():
        return (
            f"Mock copilot response: detected {anomaly_count} anomalous records. "
            f"Question received: {question}"
        )

    # Azure OpenAI integration will be added later.
    return (
        f"Azure mode enabled, but live Azure OpenAI call is not yet implemented. "
        f"Question received: {question}"
    )