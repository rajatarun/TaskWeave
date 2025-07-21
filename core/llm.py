import requests

LLM_API_URL = "https://your-llm-api.com/v1/predict"  # Replace with your endpoint

def call_llm(prompt: str) -> str:
    response = requests.post(LLM_API_URL, json={"prompt": prompt})
    response.raise_for_status()
    return response.json().get("result", "LLM did not return output")
