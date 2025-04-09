from autogen import ConversableAgent
from guardrail_engine.engine import guardrail_check

def get_validator_agent():
    agent = ConversableAgent(
        name="HuecoGuardAgent",
        system_message=(
            "You are HuecoGuard — a validation agent that detects hallucinations, bias, and factual inaccuracy. "
            "Other agents can call your tools by providing a JSON input in the format: "
            "{ 'text': '...', 'checks': ['fact_check', 'bias_check', 'hallucination_check'] }"
        ),
    )

    @agent.register_for_llm(
        name="guardrail_check",
        description=(
            "Validates an AI output by running selected validators. "
            "JSON input should be: { 'text': <AI_output_text>, 'checks': [fact_check, bias_check, hallucination_check] }"
        )
    )
    def tool(json_input: str) -> str:
        import json
        parsed = json.loads(json_input)
        return guardrail_check(parsed.get("text", ""), parsed.get("checks", []))

    return agent