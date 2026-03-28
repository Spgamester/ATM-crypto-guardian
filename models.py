from pydantic import BaseModel, Field
from typing import Literal

class Observation(BaseModel):
    transaction_id: str = Field(..., description="Unique ID for the ATM transaction.")
    atm_id: str = Field(..., description="Physical ATM terminal identifier.")
    timestamp: float = Field(..., description="Unix timestamp of the request to detect replay attacks.")
    protocol_version: str = Field(..., description="E.g., SSLv3, TLSv1.2, TLSv1.3. Useful for detecting MITM downgrade attacks.")
    encryption_type: Literal["NONE", "DES", "3DES", "AES-256"] = Field(..., description="Algorithm used for payload encryption.")
    signature_valid: bool = Field(..., description="Initial hardware signature verification status.")

class Action(BaseModel):
    decision: Literal["ALLOW", "BLOCK_TRANSACTION", "SHUTDOWN_ATM", "FLAG_FOR_REVIEW"] = Field(..., description="The defensive action to take.")
    reason: str = Field(..., description="Explanation for the decision, mapping back to the specific attack vector.")

class Reward(BaseModel):
    score: float = Field(..., description="Reward signal: +1.0 for correct defense/allow, -1.0 for false positive/negative.")
    feedback: str = Field(..., description="Environment feedback on the action taken.")
    is_done: bool = Field(..., description="True if the task is complete and there are no more transactions to process.")