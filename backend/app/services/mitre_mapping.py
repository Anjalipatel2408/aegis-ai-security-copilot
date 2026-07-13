MITRE_ATTACK_MAP = {
    "brute_force": {
        "technique_id": "T1110",
        "technique_name": "Brute Force",
        "tactic": "Credential Access"
    },
    "sql_injection": {
        "technique_id": "T1190",
        "technique_name": "Exploit Public-Facing Application",
        "tactic": "Initial Access"
    },
    "ddos": {
        "technique_id": "T1499",
        "technique_name": "Endpoint Denial of Service",
        "tactic": "Impact"
    },
    "phishing": {
        "technique_id": "T1566",
        "technique_name": "Phishing",
        "tactic": "Initial Access"
    },
    "unauthorized_access": {
        "technique_id": "T1078",
        "technique_name": "Valid Accounts",
        "tactic": "Defense Evasion"
    },
    "unknown": {
        "technique_id": "N/A",
        "technique_name": "Unclassified Activity",
        "tactic": "N/A"
    }
}

def get_mitre_info(attack_type):
    return MITRE_ATTACK_MAP.get(attack_type, MITRE_ATTACK_MAP["unknown"])