import os
import json
from autogen.agentchat import ConversableAgent
from guardrail_engine.engine import guardrail_check  # Your actual function

def get_validator_agent():
    llm_config = {
        "config_list": [
            {
                "model": "gpt-4",
                "api_key": os.getenv("OPENAI_API_KEY"),
                "base_url": "https://api.openai.com/v1",
            }
        ],
        "temperature": 0.7,
        "timeout": 30,
    }

    agent = ConversableAgent(
        name="HuecoGuardAgent",
        system_message=(
            "You are HuecoGuard — a validation agent that detects hallucinations, bias, and factual inaccuracy. "
            "Other agents can call your tools by providing a JSON input like: "
            "{ 'text': '...', 'checks': ['fact_check', 'bias_check', 'hallucination_check'] }"
        ),
        llm_config=llm_config,
    )

    # Define the tool function.
    def tool(json_input: str) -> str:
        parsed = json.loads(json_input)
        return guardrail_check(parsed.get("text", ""), parsed.get("checks", []))

    # First, try to register using the built-in method if available.
    if hasattr(agent, "register_tool"):
        agent.register_tool("guardrail_check", tool, "Validates text using fact, bias, and hallucination checks.")
    else:
        # Fallback: manually add to the function_map.
        agent.function_map["guardrail_check"] = tool

    return agent
