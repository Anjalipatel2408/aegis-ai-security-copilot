from collections import Counter
from app.services.mitre_mapping import get_mitre_info

def classify_attack(entry, all_entries):
    """
    Simple rule-based classification.
    entry: single ParsedLogEntry object (anomalous)
    all_entries: all entries from same log file (for context, e.g. repeat count)
    """
    ip_counts = Counter([e.ip_address for e in all_entries if e.ip_address])
    same_ip_count = ip_counts.get(entry.ip_address, 0)

    endpoint = (entry.endpoint or "").lower()
    status = entry.status_code or ""

    # Rule-based detection (સાદા rules -- પછી વધુ sophisticated બનાવી શકાય)
    if same_ip_count > 5 and status in ["401", "403"]:
        attack_type = "brute_force"
    elif "select" in endpoint or "union" in endpoint or "--" in endpoint:
        attack_type = "sql_injection"
    elif same_ip_count > 20:
        attack_type = "ddos"
    elif "login" in endpoint and status == "200" and same_ip_count == 1:
        attack_type = "unauthorized_access"
    else:
        attack_type = "unknown"

    mitre_info = get_mitre_info(attack_type)

    return {
        "attack_type": attack_type,
        "mitre_technique_id": mitre_info["technique_id"],
        "mitre_technique_name": mitre_info["technique_name"],
        "mitre_tactic": mitre_info["tactic"]
    }