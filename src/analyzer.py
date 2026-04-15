import re
from collections import Counter

LOG_FILE = 'logs/app.log'

def analyze_logs():
    errors = []
    info_count = 0

    with open(LOG_FILE, "r") as f:
        for line in f:
            if "ERROR" in line:
                errors.append(line.strip())
            elif "INFO" in line:
                info_count += 1

    error_types = Counter(errors)

    report = {
        "total_info_logs": info_count,
        "total_errors": len(errors),
        "error_details": list(errors)
    }

    return report

if __name__ == "__main__":
    result = analyze_logs()
    print("Log Analysis Result:")
    print(result)