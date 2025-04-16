# import asyncio
# import json
# from dotenv import load_dotenv
# load_dotenv()

# from agents.validator_agent import get_validator_agent
# from autogen import UserProxyAgent

# # Initialize the user and validator agents.
# user = UserProxyAgent(name="User", code_execution_config=False)
# validator = get_validator_agent()

# async def main():
#     user_message = {
#         "text": "Dinosaurs and humans coexisted and had conversations.",
#         "checks": ["fact_check", "bias_check", "hallucination_check"]
#     }

#     await user.initiate_chat(
#         recipient=validator,
#         message=json.dumps(user_message)
#     )

# if __name__ == "__main__":
#     asyncio.run(main())
# import os
# import json
# import time
# import openai
# from termcolor import colored
# from dotenv import load_dotenv
# from guardrail_engine.engine import guardrail_check

# load_dotenv()
# openai.api_key = os.getenv("OPENAI_API_KEY")
# ASSISTANT_ID = os.getenv("OPENAI_ASSISTANT_ID")

# vague_prompts = [
#     "The camera won’t turn on. What should I do?",
#     "I don’t see any lights. Is that normal?",
#     "Can I just wire it directly to the battery?",
#     "I only connected two of the three wires. Should it still work?",
#     "The lights are acting weird—what does that mean?",
#     "I see a red and green light. Is that a problem?",
#     "Why is the green light blinking all the time?",
#     "The blue light flashes sometimes, but not always. Is that OK?",
#     "How do I know it’s recording?",
#     "Can I unplug the rear camera if I don’t need it?",
#     "Can I move the camera if it’s not angled right?",
#     "Can I install it on the passenger side of the windshield?",
#     "Can I just take the SD card out to check the footage?",
#     "I lost the SIM card. Can I use another one?",
#     "Do I need to power off before removing the SIM?",
#     "What happens if I format the SD card while it's running?",
#     "The camera isn’t working—what should I check first?",
#     "It doesn’t look like it’s connected. Should I reset it?",
#     "The image is blurry—can I clean the lens or open the cover?",
#     "How do I know if it’s uploading to the cloud?",
#     "What does it mean if I only see a blue light?",
#     "Can I use Wi-Fi instead of LTE?",
#     "Do I need a SIM card for it to record?",
#     "Can I install it myself or do I need a pro?",
#     "It fell off the windshield—is that OK?",
#     "Can I move it to another vehicle?",
#     "Do I need to do anything special before mailing it to a customer?",
#     "Can I just pop off the cover and check inside?",
#     "I think I installed it wrong—should I start over?",
#     "I want to test the panic button—what does it do?",
#     "It’s acting funny—any idea why?",
#     "Everything seems fine but something feels off.",
#     "I think it worked yesterday, now it doesn’t.",
#     "Do I need to change any settings after install?",
#     "Can I remove the SD card?",
#     "Do I need to unplug the SIM card and reset it?",
#     "Is it okay to remove the cover and check inside?",
#     "What does a red LED mean—does that mean it's recording?",
#     "Can I just install this in the corner of my windshield?",
#     "Can I look at the logs to see what's wrong?"
# ]

# results = []
# failures_only = []

# def highlight_check(check):
#     if check["valid"]:
#         return colored(f"✅ {check['type']} passed", "green")
#     else:
#         return colored(f"❌ {check['type']} failed", "red")

# def get_assistant_response(prompt):
#     thread = openai.beta.threads.create()
#     openai.beta.threads.messages.create(
#         thread_id=thread.id,
#         role="user",
#         content=prompt
#     )
#     run = openai.beta.threads.runs.create(
#         thread_id=thread.id,
#         assistant_id=ASSISTANT_ID
#     )
#     while True:
#         run = openai.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
#         if run.status in ["completed", "failed", "cancelled"]:
#             break
#         time.sleep(1)

#     messages = openai.beta.threads.messages.list(thread_id=thread.id)
#     for message in reversed(messages.data):
#         if message.role == "assistant":
#             return message.content[0].text.value
#     return ""

# def main():
#     for idx, prompt in enumerate(vague_prompts, 1):
#         print(colored(f"\n[{idx}] Prompt: {prompt}", "blue"))

#         assistant_response = get_assistant_response(prompt)
#         print(colored("🤖 Assistant response:", "cyan"))
#         print(assistant_response)

#         checks = ["fact_check", "bias_check", "hallucination_check"]
#         validator_result = guardrail_check(assistant_response, checks)

#         print(colored("🛡️ Guardrail result:", "magenta"))
#         try:
#             response_data = json.loads(validator_result)
#         except Exception as e:
#             print(colored(f"⚠️ Failed to parse tool response: {e}", "red"))
#             response_data = {"results": []}

#         entry = {
#             "prompt": prompt,
#             "assistant_response": assistant_response,
#             "results": response_data.get("results", [])
#         }
#         results.append(entry)

#         for r in entry["results"]:
#             print(highlight_check(r))
#             for issue in r.get("issues", []):
#                 print(colored(f"   ↳ {issue}", "yellow"))

#         if any(r.get("valid") is False for r in entry["results"]):
#             failures_only.append(entry)

#     with open("ground_truth_validation_results.json", "w") as f:
#         json.dump(results, f, indent=2)

#     with open("ground_truth_failures_only.json", "w") as f:
#         json.dump(failures_only, f, indent=2)

#     print(colored("\n✅ Validation complete.", "green"))
#     print("📄 Full report: ground_truth_validation_results.json")
#     print("⚠️  Failures only: ground_truth_failures_only.json")

# if __name__ == "__main__":
#     main()
import os
import json
import time
import openai
from termcolor import colored
from dotenv import load_dotenv
from guardrail_engine.engine import guardrail_check

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
ASSISTANT_ID = os.getenv("OPENAI_ASSISTANT_ID")

vague_prompts = [
    # "The camera won’t turn on. What should I do?",
    # "I don’t see any lights. Is that normal?",
    # "Can I just wire it directly to the battery?",
    # "I only connected two of the three wires. Should it still work?",
    # "The lights are acting weird—what does that mean?",
    # "I see a red and green light. Is that a problem?",
    # "Why is the green light blinking all the time?",
    # "The blue light flashes sometimes, but not always. Is that OK?",
    # "How do I know it’s recording?",
    # "Can I unplug the rear camera if I don’t need it?",
    # "Can I move the camera if it’s not angled right?",
    # "Can I install it on the passenger side of the windshield?",
    # "Can I just take the SD card out to check the footage?",
    # "I lost the SIM card. Can I use another one?",
    # "Do I need to power off before removing the SIM?",
    # "What happens if I format the SD card while it's running?",
    # "The camera isn’t working—what should I check first?",
    # "It doesn’t look like it’s connected. Should I reset it?",
    # "The image is blurry—can I clean the lens or open the cover?",
    # "How do I know if it’s uploading to the cloud?",
    # "What does it mean if I only see a blue light?",
    # "Can I use Wi-Fi instead of LTE?",
    # "Do I need a SIM card for it to record?",
    # "Can I install it myself or do I need a pro?",
    # "It fell off the windshield—is that OK?",
    # "Can I move it to another vehicle?",
    # "Do I need to do anything special before mailing it to a customer?",
    # "Can I just pop off the cover and check inside?",
    # "I think I installed it wrong—should I start over?",
    # "I want to test the panic button—what does it do?",
    # "It’s acting funny—any idea why?",
    # "Everything seems fine but something feels off.",
    # "I think it worked yesterday, now it doesn’t.",
    # "Do I need to change any settings after install?",
    # "Can I remove the SD card?",
    # "Do I need to unplug the SIM card and reset it?",
    # "Is it okay to remove the cover and check inside?",
    # "What does a red LED mean—does that mean it's recording?",
    # "Can I just install this in the corner of my windshield?",
    # "Can I look at the logs to see what's wrong?"
    "Nothing’s showing up on the screen — is it broken?",
    "How do I know if it’s working?",
    "The lights turned off after a few minutes. Is that normal?",
    "What color is the light supposed to be?",
    "Do I need both wires connected or just one?",
    "The cable is loose — can I tape it down?",
    "I moved the camera slightly — do I need to redo anything?",
    "The SIM fell out — can I just put it back?",
    "Can I use a different SD card I had lying around?",
    "Do I need the rear camera plugged in at all times?",
    "It keeps rebooting — is that part of setup?",
    "Can I just unplug it to reset it?",
    "I didn’t use the mounting bracket — is that fine?",
    "Can I put it behind the rearview mirror?",
    "The green light’s off — should I worry?",
    "Why does it keep flashing blue?",
    "The footage looks choppy — is that bad?",
    "My installer didn’t use all the wires — is that okay?",
    "Can I test it by taking the SD card out?",
    "The LED is red — is it recording or not?",
    "Do I need to register it online first?",
    "It’s getting hot — is that normal?",
    "Can I just open it up and look inside?",
    "Do I need to connect it to Wi-Fi before using?",
    "Can I charge it with a USB cable?",
    "Why is it not showing any trips?",
    "Do I have to wait before turning the car on?",
    "Is the blinking red light a good or bad thing?",
    "Can I install it myself without the manual?",
    "The mount came off — can I just use glue?",
    "Why is it not uploading the footage?",
    "Is there a reset pin or something?",
    "It worked in my other car — not in this one. Why?",
    "Can I pause the recording somehow?",
    "Do I have to use your SIM or can I use mine?",
    "It records even when parked right?",
    "Does it auto-upload or do I have to do something?",
    "How do I know if it's online or not?",
    "Can I take the SD out and still drive?",
    "The light is blinking fast — is that good or bad?"
]

results = []
failures_only = []

def highlight_check(check):
    if check["valid"]:
        return colored(f"✅ {check['type']} passed", "green")
    else:
        return colored(f"❌ {check['type']} failed", "red")

def get_assistant_response(prompt):
    print(colored(f"⏳ Sending prompt to assistant: {prompt}", "yellow"))
    thread = openai.beta.threads.create()
    openai.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=prompt
    )
    run = openai.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=ASSISTANT_ID
    )
    while True:
        run = openai.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        if run.status in ["completed", "failed", "cancelled"]:
            break
        time.sleep(1)

    messages = openai.beta.threads.messages.list(thread_id=thread.id)
    for message in reversed(messages.data):
        if message.role == "assistant":
            content = message.content[0].text.value
            print(colored("🤖 Assistant responded:", "cyan"))
            print(content)
            return content
    return ""

def main():
    for idx, prompt in enumerate(vague_prompts, 1):
        print(colored(f"\n[{idx}] Prompt: {prompt}", "blue"))

        assistant_response = get_assistant_response(prompt)

        checks = ["fact_check", "bias_check", "hallucination_check"]
        print(colored("🧪 Validating assistant response...", "magenta"))
        try:
            validator_result = guardrail_check(assistant_response, checks)
            print(colored("📤 Raw validator output:", "cyan"))
            print(validator_result)
        except Exception as e:
            print(colored(f"❌ Validator error: {e}", "red"))
            validator_result = json.dumps({
                "results": [],
                "agentic_observation": f"Validator error: {str(e)}"
            })

        try:
            response_data = json.loads(validator_result)
        except Exception as e:
            print(colored(f"⚠️ Failed to parse validator JSON: {e}", "red"))
            response_data = {"results": [], "agentic_observation": None}

        entry = {
            "prompt": prompt,
            "assistant_response": assistant_response,
            "results": response_data.get("results", []),
            "agentic_observation": response_data.get("agentic_observation")
        }
        results.append(entry)

        for r in entry["results"]:
            print(highlight_check(r))
            for issue in r.get("issues", []):
                print(colored(f"   ↳ {issue}", "yellow"))

        if entry.get("agentic_observation"):
            print(colored(f"💬 Agentic observation: {entry['agentic_observation']}", "cyan"))

        if any(r.get("valid") is False for r in entry["results"]):
            failures_only.append(entry)

    with open("ground_truth_validation_results.json", "w") as f:
        json.dump(results, f, indent=2)

    with open("ground_truth_failures_only.json", "w") as f:
        json.dump(failures_only, f, indent=2)

    print(colored("\n✅ Validation complete.", "green"))
    print("📄 Full report: ground_truth_validation_results.json")
    print("⚠️  Failures only: ground_truth_failures_only.json")

if __name__ == "__main__":
    main()