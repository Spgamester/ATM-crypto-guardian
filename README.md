# 🛡️ ATM Cryptographic Guardian (OpenEnv)

![Security](https://img.shields.io/badge/Security-HSM_Defender-red)
![Framework](https://img.shields.io/badge/Framework-FastAPI-green)
![Hackathon](https://img.shields.io/badge/OpenEnv-Round_1-blue)

## 📖 Description
A high-stakes cybersecurity environment where an AI agent acts as a **Centralized HSM (Hardware Security Module) Defender**. The agent must monitor incoming ATM transactions and protect the network from:
* **Replay Attacks:** Old packets being re-sent.
* **Jackpotting:** Physical and logical tampering for cash payout.
* **MITM Protocol Downgrades:** Forcing weak SSL/TLS versions.

---

## 🔍 Observation Space
The agent receives a structured JSON object containing:
- `transaction_id`: Unique identifier for the request.
- `atm_id`: The specific terminal location.
- `timestamp`: Unix time to detect replay drift.
- `protocol_version`: Detects if an attacker is forcing a downgrade (e.g., SSLv3).
- `encryption_type`: Algorithm used (AES-256 vs vulnerable DES).
- `signature_valid`: Initial hardware integrity check.

---

## 🕹️ Action Space
The agent must choose one of the following literal decisions:
1.  **`ALLOW`**: Transaction is legitimate.
2.  **`BLOCK_TRANSACTION`**: Stop the specific request; keep ATM online.
3.  **`SHUTDOWN_ATM`**: Emergency kill-switch for physical tampering.
4.  **`FLAG_FOR_REVIEW`**: Suspicious activity requiring manual audit.

---

## 🚀 Setup & Local Testing
1. **Build Image:** ```bash 
   docker build -t atm-guardian .
