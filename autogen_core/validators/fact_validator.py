import requests

def validate_fact(text: str) -> dict:
    try:
        response = requests.post("http://localhost:3001/validate/fact", json={"text": text})
        return response.json()
    except Exception as e:
        return {
            "type": "fact_check",
            "valid": False,
            "confidence": 0.0,
            "issues": [f"Fact check error: {str(e)}"]
        }