from src.analyzer import analyze_logs
import json
import os

def save_report(data):
    os.makedirs("reports", exist_ok=True)

    with open("reports/report.json", "w") as f:
        json.dump(data, f, indent=4)

if __name__ == "__main__":
    result = analyze_logs()
    save_report(result)
    print("Report generated ✔")