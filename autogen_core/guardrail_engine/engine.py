import json
from validators.fact_validator import validate_fact
from validators.bias_validator import validate_bias
from validators.hallucination_validator import validate_hallucination

def guardrail_check(text, checks):
    results = []

    if "fact_check" in checks:
        results.append(validate_fact(text))
    if "bias_check" in checks:
        results.append(validate_bias(text))
    if "hallucination_check" in checks:
        results.append(validate_hallucination(text))

    return json.dumps({"results": results}, indent=2)