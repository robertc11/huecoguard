import requests

def validate_bias(text: str) -> dict:
    try:
        response = requests.post("http://localhost:3002/validate/bias", json={"text": text})
        return response.json()
    except Exception as e:
        return {
            "type": "bias_check",
            "valid": False,
            "confidence": 0.0,
            "issues": [f"Bias check error: {str(e)}"]
        }