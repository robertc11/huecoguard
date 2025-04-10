# HuecoGuard

HuecoGuard is a modular AI guardrail system that ensures the accuracy, fairness, and clarity of AI-generated content. Built with Microsoft AutoGen (Python) for agent orchestration and Node.js for backend validators, HuecoGuard acts as a robust sentinel against hallucinations, bias, and factual inaccuracies.

## Inspiration

**HuecoGuard** draws its name from the Hueco Formation in Texas, celebrated for its extensive limestone deposits. Just as the formation provides a solid and enduring foundation, HuecoGuard serves as a guardian of truth, ensuring AI outputs remain reliable and free from misinformation.

## Setup and Installation

Follow these steps to set up and run HuecoGuard on your local machine.

### Prerequisites

- **Python 3.11** (or a compatible version)
- **Node.js** (for backend validators, if needed)
- An **OpenAI API key** (obtainable from [OpenAI's platform](https://platform.openai.com/))
- Git installed on your system

### Step 1: Clone the Repository

Open your terminal and clone the HuecoGuard repository:

```bash
git clone https://github.com/your_username/huecoguard.git
cd huecoguard
```

### Step 2: Create and Activate a Virtual Environment

Create a virtual environment using Python 3.11:

```bash
python3.11 -m venv new_env
source new_env/bin/activate  # On Windows use `new_env\Scripts\activate`
```

### Step 3: Install Required Packages

There is a `requirements.txt` file located in the `autogen_core` directory. Ensure your virtual environment is activated, then run:

```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

HuecoGuard requires your OpenAI API key. Create a file named `.env` in the project root (the same directory as your `main.py`) with the following content (replace with your actual API key):

```env
OPENAI_API_KEY=sk-YourActualAPIKeyHere
```

### Running the Validators

Start the validators in the following order:

1. **Fact Validator**  
   Open a new terminal tab and run the following commands:

   ```bash
   cd node_validators/fact-validator
   npm install
   echo "OPENAI_API_KEY=your-openai-api-key" > .env
   npm start
   ```

2. **Bias Validator**  
   Open a new terminal tab and run the following commands:

   ```bash
   cd node_validators/bias-validator
   npm install
   echo "OPENAI_API_KEY=your-openai-api-key" > .env
   npm start
   ```

3. **Hallucination Validator**  
   Open a new terminal tab and run the following commands:

   ```bash
   cd node_validators/hallucination-validator
   npm install
   echo "OPENAI_API_KEY=your-openai-api-key" > .env
   npm start
   ```

Simply replace `your-openai-api-key` with your actual key when you're ready to run the validators.

### Running the Main Python File

To start the HuecoGuard core system, navigate to the `autogen_core` directory and run the main Python file:

```bash
cd autogen_core
python main.py
```

Ensure that your virtual environment is activated and all required dependencies are installed before running this command.

### Using HuecoGuard with AutoGen Agents

Any AutoGen agent can call HuecoGuard by passing the required arguments to the tool. Below is an example of how to invoke HuecoGuard with the expected arguments:

```python
import asyncio
import json
from autogen import UserProxyAgent  # Import the UserProxyAgent class from AutoGen.

# Initialize the requester agent with a unique name.
requester_agent = UserProxyAgent(name="RequesterAgent", code_execution_config=False)

# Define the input text and the validation checks to perform.
validation_request = {
    "text": "The Hueco Formation was once believed to be an ancient alien landing site, as evidenced by unusual magnetic fields and perfectly symmetrical stone patterns found in the limestone.",
    "checks": ["fact_check", "bias_check", "hallucination_check"]
}

# Convert the dictionary to a JSON-formatted string.
tool_call_message = json.dumps(validation_request)

async def call_huecoguard_tool():
    # Send the validation request to the HuecoGuard agent.
    response = await requester_agent.initiate_chat(
        recipient="<HuecoGuardAgent Identifier>",  # Replace with the actual identifier of the HuecoGuard agent.
        message=tool_call_message
    )
    
    # Process and display the response received from HuecoGuard.
    print("Response from HuecoGuard:", response)

# Execute the asynchronous function.
if __name__ == '__main__':
    asyncio.run(call_huecoguard_tool())
```

In this example:
- `text` is the input content to be validated.
- `checks` is a list of validation types to perform. Supported checks include:
  - `fact_check`
  - `bias_check`
  - `hallucination_check`

The `call_huecoguard_tool` function will send the request to HuecoGuard and return a structured response indicating the results of the specified validations.

