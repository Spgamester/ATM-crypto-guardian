---
title: Cryptographic Guardian for ATM
emoji: 🛡️
colorFrom: blue
colorTo: green
sdk: docker
app_port: 7860
pinned: false
---

# 🛡️ ATM Cryptographic Guardian (Grand Finale Edition)

**A multi-step, agentic reinforcement learning environment built for the Meta PyTorch OpenEnv Hackathon x Scaler School of Technology.**

## 🚀 Advanced Architecture: Partial Observability & Agentic Workflows
Unlike standard "pass/fail" environments, the ATM Guardian environment is designed to test a Large Language Model's capacity for **multi-step reasoning, tool use, and state investigation**. 

It simulates a Centralized Hardware Security Module (HSM) defending an ATM network against protocol downgrades, replay attacks, and cryptographic forgeries.

### Key Technical Features:
1. **Hidden States (Partial Observability):** Critical cryptographic data (`encryption_status`, `hsm_signature`) is deliberately hidden from the initial observation. The AI cannot simply guess the answer.
2. **Tool-Use Requirement:** The agent must actively deploy investigation tools (`SCAN_ENCRYPTION`, `VERIFY_HSM_SIGNATURE`) to mutate the environment state and reveal hidden parameters before making a final decision.
3. **Stochastic Generation:** Transactions, timestamps, and node IDs are dynamically generated per episode, preventing the LLM from relying on memorized, static data.
4. **Strict Reward Shaping:** The environment utilizes a clamped `(0.01, 0.99)` reward schema to evaluate methodology, not just the final answer.

---

## 🧠 Environment Mechanics

### The Action Space
The agent has access to a dynamic action space divided into two phases:

**Investigation Actions (Tools):**
* `SCAN_ENCRYPTION`: Pings the payload to reveal if it is secure (AES-256) or compromised (SSLv3).
* `VERIFY_HSM_SIGNATURE`: Validates the hardware keys against the central server.

**Terminal Actions (Decisions):**
* `ALLOW_TRANSACTION`: Approves the withdrawal.
* `BLOCK_TRANSACTION`: Drops the current connection.
* `SHUTDOWN_TERMINAL`: Issues a severe network-wide lock on the specific ATM node.

### The Reward Function
To prevent "lucky guesses," the environment enforces strict penalties:
* **+0.20**: Awarded for successfully utilizing an investigation tool to reveal hidden state variables.
* **+0.95**: Awarded for executing the correct Terminal Action *after* a proper investigation.
* **+0.10 (Penalty)**: Given if the agent attempts a blind guess (executing a Terminal Action without uncovering the hidden states first).
* **+0.20 (Partial)**: Given if the agent investigates properly, but chooses the wrong Terminal Action.

---

## 📂 Project Structure

This environment is fully containerized and served via a FastAPI backend, ensuring compliance with OpenEnv infrastructure limits (2 vCPU, 8GB RAM).

```text
├── server/
│   ├── app.py
│   ├── environment.py
│   ├── models.py
├── inference.py
├── openenv.yaml
├── Dockerfile
├── pyproject.toml
├── uv.lock
└── README.md
