from fastapi import FastAPI
from models import Action, Observation, Reward
from environment import ATMEnvironment

app = FastAPI()
env = ATMEnvironment()

@app.post("/reset", response_model=Observation)
def reset(task_level: int = 1):
    return env.reset(task_level)

@app.post("/step", response_model=Reward)
def step(action: Action):
    return env.step(action)

@app.get("/state", response_model=Observation)
def state():
    return env.get_state()