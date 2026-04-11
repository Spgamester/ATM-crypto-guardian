---
title: Cryptographic Guardian for ATM
emoji: 🛡️
colorFrom: blue
colorTo: green
sdk: docker
app_port: 7860
pinned: false
---

# 🛡️ ATM Cryptographic Guardian

**A partially observable, multi-step reinforcement learning environment simulating a Centralized Hardware Security Module (HSM) defending an ATM network.**

## 📌 Overview
The ATM Guardian environment evaluates an agent's capacity for multi-step reasoning, tool use, and state investigation. It requires the agent to defend against protocol downgrades, replay attacks, and cryptographic forgeries by investigating hidden parameters before making terminal security decisions.

### Key Technical Features:
* **Partial Observability:** Critical cryptographic data (`encryption_status`, `hsm_signature`) is hidden from the initial observation state.
* **Tool-Use Integration:** The agent must deploy investigation tools (`SCAN_ENCRYPTION`, `VERIFY_HSM_SIGNATURE`) to mutate the environment state and reveal necessary parameters.
* **Stochastic Generation:** Transactions, timestamps, and node IDs are dynamically generated per episode to ensure robust evaluation.
* **Reward Shaping:** The environment utilizes a clamped `(0.01, 0.99)` reward schema to evaluate investigation methodology and terminal accuracy.

---

## 🧠 Environment Mechanics

### The Action Space
The agent interacts with the environment using a two-phase action space:

**Investigation Actions (Tools):**
* `SCAN_ENCRYPTION`: Pings the payload to reveal if it is secure (AES-256) or compromised (SSLv3).
* `VERIFY_HSM_SIGNATURE`: Validates the hardware keys against the central server.

**Terminal Actions (Decisions):**
* `ALLOW_TRANSACTION`: Approves the withdrawal.
* `BLOCK_TRANSACTION`: Drops the current connection.
* `SHUTDOWN_TERMINAL`: Issues a severe network-wide lock on the specific ATM node.

### The Reward Function
The environment enforces strict reward mapping based on the agent's methodology:
* **+0.20**: Awarded for successfully utilizing an investigation tool to reveal hidden state variables.
* **+0.95**: Awarded for executing the correct Terminal Action after conducting a proper investigation.
* **+0.10**: Applied as a penalty if the agent attempts to execute a Terminal Action without uncovering the hidden states first.
* **+0.20**: Applied if the agent investigates properly but selects the incorrect Terminal Action.

---

## 🎯 Task Levels
The environment exposes three progressively difficult scenarios:

* **Level 1:** Standard Valid Transaction vs. Timestamp Replay Attack.
* **Level 2:** Hidden Protocol Downgrade Attack (AES-256 to SSLv3).
* **Level 3:** Complete HSM Signature Forgery with anomalous connection types.

---

## 📂 Project Structure

This environment is fully containerized and served via a FastAPI backend, ensuring compliance with standard infrastructure deployments (2 vCPU, 8GB RAM).

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
