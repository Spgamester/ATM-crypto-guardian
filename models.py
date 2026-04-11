from pydantic import BaseModel, Field
from typing import Literal, Optional

class Observation(BaseModel):
    transaction_id: str
    atm_id: str
    timestamp: float
    connection_type: str
    
    encryption_status: str = Field(default="HIDDEN_REQUIRE_SCAN")
    hsm_signature_valid: Optional[bool] = Field(default=None)
    
    observation_text: str

class Action(BaseModel):
    decision: Literal[
        "SCAN_ENCRYPTION",       
        "VERIFY_HSM_SIGNATURE",  
        "ALLOW_TRANSACTION",     
        "BLOCK_TRANSACTION",     
        "SHUTDOWN_TERMINAL"      
    ]
    reason: str

class Reward(BaseModel):
    reward: float 
    feedback: str
    done: bool
