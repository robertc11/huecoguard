import requests

def validate_hallucination(text: str) -> dict:
    try:
        response = requests.post("http://localhost:3003/validate/hallucination", json={"text": text})
        return response.json()
    except Exception as e:
        return {
            "type": "hallucination_check",
            "valid": False,
            "confidence": 0.0,
            "issues": [f"Hallucination check error: {str(e)}"]
        }