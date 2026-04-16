from src.analyzer import analyze_logs
from src.alert import send_slack_alert
from src.email_alert import send_email_alert
import json
import os

ERROR_THRESHOLD = 1

def save_report(data):
    os.makedirs("reports", exist_ok=True)

    with open("reports/report.json", "w") as f:
        json.dump(data, f, indent=4)

if __name__ == "__main__":
    result = analyze_logs()
    save_report(result)

    if result["total_errors"] > ERROR_THRESHOLD:

        send_slack_alert(
            f" 🚨 Log Alert! Errors detected: {result['total_errors']}"
        )

        send_email_alert(result["total_errors"])

    print("===== Log Monitoring Report =====")
    print("Errors:", result["total_errors"])
    print("Warnings:", result["total_warnings"])
    print("Average Response Time:", result["average_response_time"], "ms")
    print("Top Endpoints:", result["top_endpoints"])