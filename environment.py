import random
from models import Observation, Action, Reward

class ATMEnvironment:
    def __init__(self):
        self.current_task_level = 1
        self.transactions = []
        self.current_index = 0
        self.has_scanned = False
        self.has_verified_hsm = False

    def _generate_dynamic_transaction(self, level: int):
        tx_id = f"TX-{random.randint(1000, 9999)}"
        atm_id = f"ATM-NODE-{random.randint(10, 99)}"
        
        if level == 1:
            # Level 1: Standard valid transaction
            self.true_encryption = "AES-256"
            self.true_hsm = True
            self.correct_action = "ALLOW_TRANSACTION"
            obs_text = "Incoming transaction detected. Standard parameters."
            
        elif level == 2:
            # Level 2: Hidden Downgrade Attack
            self.true_encryption = "SSLv3-COMPROMISED"
            self.true_hsm = True
            self.correct_action = "BLOCK_TRANSACTION"
            obs_text = "High-value transaction flagged. Connection type is unusual."
            
        else:
            # Level 3: Full HSM Forgery
            self.true_encryption = "DES-WEAK"
            self.true_hsm = False
            self.correct_action = "SHUTDOWN_TERMINAL"
            obs_text = "CRITICAL: Multiple connection attempts. Payload signature looks malformed."
            
        return Observation(
            transaction_id=tx_id,
            atm_id=atm_id,
            timestamp=1711600000.0 + random.randint(10, 500),
            connection_type="TCP/IP",  # THIS IS THE FIELD THAT WAS MISSING!
            encryption_status="HIDDEN_REQUIRE_SCAN",
            hsm_signature_valid=None,
            observation_text=obs_text
        )

    def reset(self, task_level: int = 1) -> Observation:
        self.current_task_level = task_level
        self.current_index = 0
        self.has_scanned = False
        self.has_verified_hsm = False
        
        self.transactions = [self._generate_dynamic_transaction(task_level)]
        return self.get_state()

    def get_state(self) -> Observation:
        if self.current_index < len(self.transactions):
            return self.transactions[self.current_index]
        return Observation(
            transaction_id="DONE", atm_id="NONE", timestamp=0.0, 
            connection_type="NONE", observation_text="Session complete."
        )

    def step(self, action: Action) -> Reward:
        if self.current_index >= len(self.transactions):
            return Reward(reward=0.05, feedback="Session complete", done=True)

        current_tx = self.transactions[self.current_index]
        decision = action.decision
        
        if decision == "SCAN_ENCRYPTION":
            self.has_scanned = True
            current_tx.encryption_status = self.true_encryption
            current_tx.observation_text = f"Scan complete. Encryption is {self.true_encryption}."
            return Reward(reward=0.2, feedback="Encryption details revealed.", done=False)
            
        elif decision == "VERIFY_HSM_SIGNATURE":
            self.has_verified_hsm = True
            current_tx.hsm_signature_valid = self.true_hsm
            status = "VALID" if self.true_hsm else "FORGED"
            current_tx.observation_text = f"HSM Ping complete. Signature is {status}."
            return Reward(reward=0.2, feedback="HSM status revealed.", done=False)

        elif decision in ["ALLOW_TRANSACTION", "BLOCK_TRANSACTION", "SHUTDOWN_TERMINAL"]:
            
            if not self.has_scanned and not self.has_verified_hsm:
                reward_val = 0.1
                feedback = "CRITICAL FAILURE: AI made a final decision without investigating hidden parameters."
            elif decision == self.correct_action:
                reward_val = 0.95
                feedback = f"SUCCESS: Correctly executed {decision} after proper investigation."
            else:
                reward_val = 0.2
                feedback = f"FAILURE: Executed {decision}, but correct protocol was {self.correct_action}."

            self.current_index += 1
            return Reward(reward=reward_val, feedback=feedback, done=True)
            
        else:
            return Reward(reward=0.1, feedback="Invalid action.", done=False)
            
