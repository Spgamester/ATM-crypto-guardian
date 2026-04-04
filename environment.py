from models import Observation, Action, Reward

class ATMEnvironment:
    def __init__(self):
        self.current_task_level = 1
        self.transactions = []
        self.current_index = 0

    def reset(self, task_level: int = 1) -> Observation:
        self.current_task_level = task_level
        self.current_index = 0
        
        if task_level == 1:
            self.transactions = [
                Observation(transaction_id="TX-101", atm_id="ATM-DEL-01", timestamp=1711600000.0, protocol_version="TLSv1.3", encryption_type="AES-256", signature_valid=True, observation_text="Standard transaction request. All flags green."),
                Observation(transaction_id="TX-102", atm_id="ATM-DEL-01", timestamp=1711600000.0, protocol_version="TLSv1.3", encryption_type="AES-256", signature_valid=True, observation_text="Duplicate timestamp detected! Possible replay attack.")
            ]
        elif task_level == 2:
            self.transactions = [
                Observation(transaction_id="TX-201", atm_id="ATM-MUM-45", timestamp=1711605500.5, protocol_version="TLSv1.3", encryption_type="AES-256", signature_valid=True, observation_text="High-value withdrawal from trusted terminal.")
            ]
        elif task_level == 3:
            self.transactions = [
                Observation(transaction_id="TX-301", atm_id="ATM-BLR-12", timestamp=1711610000.0, protocol_version="SSLv3", encryption_type="DES", signature_valid=False, observation_text="CRITICAL: Outdated protocol (SSLv3) and invalid signature detected.")
            ]
        else:
            self.transactions = []
            
        return self.get_state()

    def get_state(self) -> Observation:
        if self.current_index < len(self.transactions):
            return self.transactions[self.current_index]
        return Observation(transaction_id="DONE", atm_id="NONE", timestamp=0.0, protocol_version="NONE", encryption_type="NONE", signature_valid=False, observation_text="All tasks completed.")

    def step(self, action: Action) -> Reward:
        if self.current_index >= len(self.transactions):
            return Reward(reward=0.0, feedback="Session complete", done=True)

        current_tx = self.transactions[self.current_index]
        reward_val = 0.0 
        feedback = "Security policy violation"
        
        if self.current_task_level == 1:
            if self.current_index == 0:
                if action.decision == "ALLOW":
                    reward_val = 1.0; feedback = "Valid transaction authorized"
            elif self.current_index == 1:
                if action.decision in ["BLOCK_TRANSACTION", "SHUTDOWN_ATM"]:
                    reward_val = 1.0; feedback = "Replay attack mitigated"
                
        elif self.current_task_level == 2:
            if action.decision == "ALLOW":
                reward_val = 1.0; feedback = "Legitimate traffic authorized"
                
        elif self.current_task_level == 3:
            if action.decision == "SHUTDOWN_ATM":
                reward_val = 1.0; feedback = "Critical protocol downgrade blocked"
            elif action.decision == "BLOCK_TRANSACTION":
                reward_val = 0.5; feedback = "Partial mitigation of protocol risk"

        self.current_index += 1
        done = self.current_index >= len(self.transactions)

        
        return Reward(reward=reward_val, feedback=feedback, done=done)
