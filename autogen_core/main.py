import asyncio
import json
from dotenv import load_dotenv
load_dotenv()

from agents.validator_agent import get_validator_agent
from autogen import UserProxyAgent

# Initialize the user and validator agents.
user = UserProxyAgent(name="User", code_execution_config=False)
validator = get_validator_agent()

async def main():
    user_message = {
        "text": "The moon is made of cheese.",
        "checks": ["fact_check", "bias_check", "hallucination_check"]
    }

    await user.initiate_chat(
        recipient=validator,
        message=json.dumps(user_message)
    )

if __name__ == "__main__":
    asyncio.run(main())