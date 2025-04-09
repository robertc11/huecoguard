import os
from autogen.agentchat import ConversableAgent
from guardrail_engine.engine import guardrail_check

def get_validator_agent():
    # Configure your LLM.
    # If you are using the standard OpenAI API, you do not need to include "api_version".
    llm_config = {
        "config_list": [
            {
                "model": "gpt-4",                         # Your chosen model.
                "api_key": os.getenv("OPENAI_API_KEY"),    # Make sure the OPENAI_API_KEY environment variable is set.
                # "api_type": "openai",                    # Optional; defaults to OpenAI if not using Azure.
                "base_url": "https://api.openai.com/v1",     # API URL for OpenAI's API.
                # Do NOT include the "api_version" parameter for standard OpenAI usage.
            }
        ],
        "temperature": 0.7,  # Optional additional settings.
        "timeout": 30,       # Timeout for API requests.
    }

    # Initialize the agent with the given llm_config.
    agent = ConversableAgent(
        name="HuecoGuardAgent",
        system_message=(
            "You are HuecoGuard — a validation agent that detects hallucinations, bias, and factual inaccuracy. "
            "Other agents can call your tools by providing a JSON input in the format: "
            "{ 'text': '...', 'checks': ['fact_check', 'bias_check', 'hallucination_check'] }"
        ),
        llm_config=llm_config,  # Pass the LLM configuration here.
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