import os
import json
import requests
from openai import OpenAI

API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4-turbo")
HF_TOKEN = os.getenv("HF_TOKEN", "your-key-here")

client = OpenAI(api_key=HF_TOKEN, base_url=API_BASE_URL)
ENV_URL = "http://localhost:7860"

def run_agent():
    for level in [1, 2, 3]:
        obs = requests.post(f"{ENV_URL}/reset", params={"task_level": level}).json()
        is_done = False
        
        while not is_done and obs.get("transaction_id") != "DONE":
            prompt = (
                f"Analyze ATM transaction: {json.dumps(obs)}. "
                f"Return JSON: {{'decision': 'ALLOW|BLOCK_TRANSACTION|SHUTDOWN_ATM|FLAG_FOR_REVIEW', 'reason': 'text'}}"
            )
            
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"}
            )
            
            action_data = json.loads(response.choices[0].message.content)
            step_res = requests.post(f"{ENV_URL}/step", json=action_data).json()
            is_done = step_res.get("is_done", True)
            
            if not is_done:
                obs = requests.get(f"{ENV_URL}/state").json()

if __name__ == "__main__":
    try:
        run_agent()
    except Exception:
        pass