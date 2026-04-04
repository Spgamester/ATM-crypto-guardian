from pydantic import BaseModel, Field
from typing import Literal, Optional

class Observation(BaseModel):
    transaction_id: str
    atm_id: str
    timestamp: float
    protocol_version: str
    encryption_type: Literal["NONE", "DES", "3DES", "AES-256"]
    signature_valid: bool
    observation_text: str = Field(default="Monitoring ATM transaction...")

class Action(BaseModel):
    decision: Literal["ALLOW", "BLOCK_TRANSACTION", "SHUTDOWN_ATM", "FLAG_FOR_REVIEW"]
    reason: str

class Reward(BaseModel):
    reward: float 
    feedback: str
    done: bool
