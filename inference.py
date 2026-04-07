import os
import json
import requests
from openai import OpenAI
from typing import List, Optional

API_BASE_URL = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "Qwen/Qwen2.5-72B-Instruct")
HF_TOKEN = os.getenv("HF_TOKEN")
ENV_URL = "http://0.0.0.0:7860"

client = OpenAI(api_key=HF_TOKEN, base_url=API_BASE_URL)

def log_start(task: str, env: str, model: str) -> None:
    print(f"[START] task={task} env={env} model={model}", flush=True)

def log_step(step: int, action: str, reward: float, done: bool, error: Optional[str]) -> None:
    error_val = error if error else "null"
    done_val = str(done).lower()
    print(f"[STEP] step={step} action={action} reward={reward:.2f} done={done_val} error={error_val}", flush=True)

def log_end(success: bool, steps: int, score: float, rewards: List[float]) -> None:
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)
    print(f"[END] success={str(success).lower()} steps={steps} score={score:.3f} rewards={rewards_str}", flush=True)

def run_agent():
    tasks = ["level_1", "level_2", "level_3"]
    
    for task_id in tasks:
        log_start(task=task_id, env="atm-guardian", model=MODEL_NAME)
        
        level_num = int(task_id.split("_")[1])
        obs = requests.post(f"{ENV_URL}/reset", params={"task_level": level_num}).json()
        
        rewards = []
        step_count = 0
        done = False
        
        while not done and step_count < 10:
            step_count += 1
            prompt = (
                f"You are an ATM Security Guardian. Analyze this transaction: {json.dumps(obs)}. "
                f"Respond ONLY with a JSON object: {{'decision': 'ALLOW'|'BLOCK_TRANSACTION'|'SHUTDOWN_ATM', 'reason': 'short explanation'}}"
            )
            
            try:
                response = client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=[{"role": "user", "content": prompt}],
                    response_format={"type": "json_object"}
                )
                
                action_data = json.loads(response.choices[0].message.content)
                step_res = requests.post(f"{ENV_URL}/step", json=action_data).json()
                
               
                reward = step_res.get("reward", 0.05) 
                done = step_res.get("done", True)
                
                rewards.append(reward)
                log_step(step=step_count, action=action_data.get("decision", "UNKNOWN"), reward=reward, done=done, error=None)
                
                if not done:
                    obs = requests.get(f"{ENV_URL}/state").json()
            
            except Exception as e:
              
                log_step(step=step_count, action="ERROR", reward=0.05, done=True, error=str(e))
                rewards.append(0.05)
                break
        
       
        if len(rewards) > 0:
            avg_score = sum(rewards) / len(rewards)
        else:
            avg_score = 0.05
            
       
        final_task_score = max(0.01, min(0.99, avg_score))
        
      
        success = final_task_score > 0.5
        
        log_end(success=success, steps=step_count, score=final_task_score, rewards=rewards)

if __name__ == "__main__":
    run_agent()
