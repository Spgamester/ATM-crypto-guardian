import os
import requests
import json
from openai import OpenAI

# Set up environment via required variables
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4-turbo")
HF_TOKEN = os.getenv("HF_TOKEN", "fake-local-key")

# Set up OpenAI client as required by OpenEnv
client = OpenAI(api_key=HF_TOKEN, base_url=API_BASE_URL)

# Set to where your local FastAPI service is running
ENV_URL = "http://localhost:7860"

def run_agent():
    print("Initializing Global ATM Fleet Cryptographic Guardian Agent...\n")

    for level in [1, 2, 3]:
        print(f"========== RUNNING TASK LEVEL {level} ==========")

        # Step 1: reset environment for this task level
        obs_response = requests.post(f"{ENV_URL}/reset?task_level={level}")
        obs = obs_response.json()

        is_done = False
        while not is_done and obs.get("transaction_id") != "DONE":
            print(f"Observing TX: {obs['transaction_id']} at {obs['atm_id']}")

            # Step 2: Construct LLM prompt with our
Analyze this incoming transaction observation:
            {json.dumps(obs, indent=2)}

            Based on the timestamp, protocol version, and encryption type, decide if this is a legitimate request, a replay attack, or a cryptographic downgrade (MITM).

            You must return a JSON object with exactly these two keys:
            - "decision": Must be strictly one of: "ALLOW", "BLOCK_TRANSACTION", "SHUTDOWN_ATM", or "FLAG_FOR_REVIEW".
            - "reason": A brief technical justification for your choice.
            """

            # Step 3: query the model
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[{"role": "user", "content": prompt}],
                response_format={ "type": "json_object" }
            )

            # Interpret the AI's instruction
            action_data = json.loads(response.choices[0].message.content)
            print(f"Agent Action: {action_data['decision']} - {action_data['reason']}")

            # Step 4: advance the environment with the chosen action
            step_response = requests.post(f"{ENV_URL}/step", json=action_data)
            reward = step_response.json()
            print(f"Reward Score: {reward['score']} | Feedback: {reward['feedback']}\n")

            is_done = reward["is_done"]

            # If the episode isn’t finished, refresh the observation
            if not is_done:
                obs = requests.get(f"{ENV_URL}/state").json()

if __name__ == "__main__":
    # Quick reachability check before starting
    try:
        requests.get(f"{ENV_URL}/state")
        run_agent()