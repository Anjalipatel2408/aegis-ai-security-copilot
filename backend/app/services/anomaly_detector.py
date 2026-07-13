import pandas as pd
from sklearn.ensemble import IsolationForest
from collections import Counter

def detect_anomalies(parsed_entries):
    """
    parsed_entries: list of ParsedLogEntry database objects
    """
    if len(parsed_entries) < 5:
        # ઓછા data હોય તો ML model ઠીક રીતે train નહીં થાય
        return {entry.id: 1 for entry in parsed_entries}

    # Features બનાવવા: IP frequency, status code, hour of day
    ip_counts = Counter([e.ip_address for e in parsed_entries if e.ip_address])

    data = []
    entry_ids = []
    for entry in parsed_entries:
        ip_freq = ip_counts.get(entry.ip_address, 0)
        status = int(entry.status_code) if entry.status_code and entry.status_code.isdigit() else 0
        hour = entry.timestamp.hour if entry.timestamp else 0

        data.append([ip_freq, status, hour])
        entry_ids.append(entry.id)

    df = pd.DataFrame(data, columns=["ip_frequency", "status_code", "hour"])

    model = IsolationForest(contamination=0.15, random_state=42)
    predictions = model.fit_predict(df)  # returns -1 (anomaly) or 1 (normal)

    return dict(zip(entry_ids, predictions))