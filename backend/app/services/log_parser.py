import re
from datetime import datetime

LOG_PATTERN = re.compile(
    r'(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) '
    r'\[(?P<level>\w+)\] '
    r'(?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) '
    r'(?P<method>\w+) '
    r'(?P<endpoint>\S+) - '
    r'(?P<status>\d{3})'
)

def parse_log_file(file_path):
    parsed_entries = []

    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            match = LOG_PATTERN.match(line)
            if match:
                data = match.groupdict()
                parsed_entries.append({
                    "timestamp": datetime.strptime(data["timestamp"], "%Y-%m-%d %H:%M:%S"),
                    "level": data["level"],
                    "ip_address": data["ip"],
                    "method": data["method"],
                    "endpoint": data["endpoint"],
                    "status_code": data["status"],
                    "raw_line": line
                })
            else:
                # જે line pattern match ના થાય, એ raw_line તરીકે જ save કરીશું
                parsed_entries.append({
                    "timestamp": None,
                    "level": None,
                    "ip_address": None,
                    "method": None,
                    "endpoint": None,
                    "status_code": None,
                    "raw_line": line
                })

    return parsed_entries