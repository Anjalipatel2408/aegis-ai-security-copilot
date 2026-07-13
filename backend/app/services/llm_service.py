import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-flash-latest",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

def get_remediation_advice(attack_type, mitre_technique, ip_address, endpoint):
    prompt = f"""
You are a cybersecurity SOC analyst assistant. An anomaly was detected:

- Attack Type: {attack_type}
- MITRE ATT&CK Technique: {mitre_technique}
- Source IP: {ip_address}
- Targeted Endpoint: {endpoint}

Provide a concise, actionable remediation plan (3-5 steps) that a SOC analyst should take right now.
"""
    response = llm.invoke(prompt)
    return response.content