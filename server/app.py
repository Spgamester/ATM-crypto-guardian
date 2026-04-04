from fastapi import FastAPI
from models import Action, Observation, Reward
from environment import ATMEnvironment

app = FastAPI()
env = ATMEnvironment()

@app.post("/reset", response_model=Observation)
def reset():
    return env.reset()
    
@app.post("/step", response_model=Reward)
def step(action: Action):
    return env.step(action)

@app.get("/state", response_model=Observation)
def state():
    return env.get_state()
def main():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)

if __name__ == "__main__":
    main()
