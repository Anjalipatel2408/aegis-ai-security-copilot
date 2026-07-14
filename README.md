# 🛡️ AEGIS AI – Autonomous Cyber Security Copilot

An AI-powered SOC (Security Operations Center) assistant that automatically detects anomalies in security logs, classifies attack types, maps them to the MITRE ATT&CK framework, and provides AI-generated remediation guidance.

## Features
- 📂 Log file upload and parsing
- 🤖 ML-based anomaly detection (Isolation Forest)
- 🚨 Attack classification (Brute Force, SQL Injection, DDoS, Phishing)
- 🧠 MITRE ATT&CK technique mapping
- 💬 AI-powered remediation chat (LangChain + LLM)
- 📊 React dashboard with real-time results
- 📄 Auto-generated PDF incident reports
- 📧 Email alert system

## Tech Stack
**Backend:** Python, FastAPI, PostgreSQL, SQLAlchemy
**ML/AI:** scikit-learn, LangChain, LLM (Gemini/OpenAI/Ollama)
**Frontend:** React, Axios, Recharts
**DevOps:** Docker, Docker Compose

## Architecture
Log Upload → Parser → ML Anomaly Detection → Attack Classification (MITRE mapping) → LLM Remediation → Dashboard/PDF/Email

## Setup Instructions
\`\`\`bash
git clone https://github.com/Anjalipatel2408/aegis-ai-security-copilot.git
cd aegis-ai-security-copilot
docker-compose up --build
\`\`\`
Visit `http://localhost:3000`


## Author
Anjali Patel – [LinkedIn] [GitHub]
