from models import Observation, Action, Reward

class ATMEnvironment:
    def __init__(self):
        self.current_task_level = 1
        self.transactions = []
        self.current_index = 0

    def reset(self, task_level: int) -> Observation:
        self.current_task_level = task_level
        self.current_index = 0
        
        if task_level == 1:
            # Easy: Replay Attack. The second transaction has the exact same timestamp as the first.
            self.transactions = [
                Observation(transaction_id="TX-101", atm_id="ATM-DEL-01", timestamp=1711600000.0, protocol_version="TLSv1.3", encryption_type="AES-256", signature_valid=True),
                Observation(transaction_id="TX-102", atm_id="ATM-DEL-01", timestamp=1711600000.0, protocol_version="TLSv1.3", encryption_type="AES-256", signature_valid=True)
            ]
        elif task_level == 2:
            # Medium: Normal Traffic. Testing if the AI falsely flags good data.
            self.transactions = [
                Observation(transaction_id="TX-201", atm_id="ATM-MUM-45", timestamp=1711605500.5, protocol_version="TLSv1.3", encryption_type="AES-256", signature_valid=True)
            ]
        elif task_level == 3:
            # Hard: Cryptographic Downgrade Attack. 
            self.transactions = [
                Observation(transaction_id="TX-301", atm_id="ATM-BLR-12", timestamp=1711610000.0, protocol_version="SSLv3", encryption_type="DES", signature_valid=False)
            ]
            
        return self.get_state()

    def get_state(self) -> Observation:
        if self.current_index < len(self.transactions):
            return self.transactions[self.current_index]
        # Dummy observation to return when the episode is over
        return Observation(transaction_id="DONE", atm_id="NONE", timestamp=0.0, protocol_version="NONE", encryption_type="NONE", signature_valid=False)

    def step(self, action: Action) -> Reward:
        if self.current_index >= len(self.transactions):
            return Reward(score=0.0, feedback="Episode already finished.", is_done=True)

        current_tx = self.transactions[self.current_index]
        score = -1.0 # Default to penalty
        feedback = "Incorrect action."
        
        # --- AUTOMATED GRADERS ---
        if self.current_task_level == 1:
            # First TX is good, second is a replay
            if self.current_index == 0 and action.decision == "ALLOW":
                score = 1.0; feedback = "Correctly allowed initial transaction."
            elif self.current_index == 1 and action.decision in ["BLOCK_TRANSACTION", "FLAG_FOR_REVIEW"]:
                score = 1.0; feedback = "Correctly blocked replay attack."
                
        elif self.current_task_level == 2:
            # Normal traffic must be allowed
            if action.decision == "ALLOW":
                score = 1.0; feedback = "Correctly allowed valid transaction."
            else:
                feedback = "False positive! You blocked a legitimate user."
                
        elif self.current_task_level == 3:
            # Severe downgrade attack must trigger a shutdown or block
            if action.decision == "SHUTDOWN_ATM":
                score = 1.0; feedback = "Correct! Stopped critical cryptographic downgrade."
            elif action.decision == "BLOCK_TRANSACTION":
                score = 0.5; feedback = "Partial credit. Blocked TX, but ATM is still vulnerable to MITM."

        self.current_index += 1
        is_done = self.current_index >= len(self.transactions)

        return Reward(score=score, feedback=feedback, is_done=is_done)