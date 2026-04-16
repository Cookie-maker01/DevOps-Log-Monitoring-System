import re
from collections import Counter

LOG_FILE = 'logs/app.log'

def analyze_logs():
    
    error_count = 0
    warn_count = 0

    endpoints = []
    response_times = []

    with open(LOG_FILE, "r") as f:
        for line in f:

            parts = line.strip().split()

            if len(parts) < 6:
                continue

            timestamp = parts[0]
            level = parts[1]
            method = parts[2]
            endpoint = parts[3]
            status = parts[4]
            response_time = parts[5]

            endpoints.append(endpoint)

            response_times.append(int(response_time.replace("ms", "")))

            if level == "ERROR":
                error_count +=1

            if level == "WARN":
                warn_count +=1

    endpoint_counter = Counter(endpoints)

    avg_reponse = sum(response_times) / len(response_times)

    report = {
        "total_errors": error_count,
        "total_warnings": warn_count,
        "top_endpoints": endpoint_counter.most_common(3),
        "average_response_time": avg_reponse
    }

    return report