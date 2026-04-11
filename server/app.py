import uvicorn
from fastapi import FastAPI, Request
from environment import ATMEnvironment
from models import Action

app = FastAPI()
env = ATMEnvironment()

@app.get("/")
async def health_check():
    return {"status": "ok", "environment": "ATM Cryptographic Guardian"}

@app.post("/reset")
async def reset(request: Request):
    """
    Bulletproof reset endpoint. It will gracefully handle query params, 
    JSON bodies, or empty requests without throwing a 422 Validation Error.
    """
    task_level = 1
    
    try:
        body = await request.json()
        task_level = body.get("task_level", 1)
    except Exception:
        pass

    try:
        task_level = int(request.query_params.get("task_level", task_level))
    except Exception:
        pass
        
    state = env.reset(task_level=task_level)
    return state.model_dump() if hasattr(state, "model_dump") else state.dict()

@app.post("/step")
async def step(action: Action):
    reward = env.step(action)
    return reward.model_dump() if hasattr(reward, "model_dump") else reward.dict()

@app.get("/state")
async def state():
    state_obj = env.get_state()
    return state_obj.model_dump() if hasattr(state_obj, "model_dump") else state_obj.dict()


def main():
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860)

if __name__ == "__main__":
    main()
