import asyncio
from dotenv import load_dotenv  # Import load_dotenv from python-dotenv
load_dotenv()  # This loads environment variables from your .env file

from agents.validator_agent import get_validator_agent
from autogen import UserProxyAgent

# Initialize the user and validator agents.
user = UserProxyAgent(name="User", code_execution_config=False)
validator = get_validator_agent()

async def main():
    # This JSON simulates an external agent request.
    user_message = {
        "text": "The moon is made of cheese.",
        "checks": ["fact_check", "bias_check", "hallucination_check"]
    }

    await user.initiate_chat(
        recipient=validator,
        message=str(user_message)
    )

if __name__ == "__main__":
    asyncio.run(main())