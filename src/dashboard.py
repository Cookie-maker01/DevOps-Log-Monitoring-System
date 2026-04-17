from flask import Flask, jsonify
import json
import threading
import time

app = Flask(__name__)

live_data = {
    "errors": 0,
    "history": []
}

def load_report():
    try:
        with open("reports/report.json", "r") as f:
            return json.load(f)
    except:
        return {}
    
LOG_FILE = "logs/app.log"

def follow(file):
    file.seek(0, 2)

    while True:
        line = file.readline()
        if not line:
            time.sleep(1)
            continue
        yield line

def stream_logs():

    print("Streaming started...")

    with open(LOG_FILE, "r") as f:

        for line in follow(f):

            parts = line.strip().split()

            if len(parts) < 6:
                continue

            level = parts[1]

            if level == "ERROR":
                live_data["errors"] += 1

            live_data["history"].append(live_data["errors"])

            if len(live_data["history"]) > 20:
                live_data["history"].pop(0)
    
@app.route("/")
def home():

    return """
<!DOCTYPE html>
<html>
<head>
    <title>DevOps Dashboard</title>
    <script src="https://cdn.jsdeliver.net/npm/chart.js"></script>
</head>

<body>
    <h1>DevOpes Log Dashboard</h1>

    <canvas id="errorChart" width="400" height="200"></canvas>

    <script>

        async function loadData() {
            const res = await fetch('/api.report');
            return await res.json();
        }

        async function renderChart() {
        
            const data = await loadData();
            
            const ctx = document.getElementById('errorChart').getContext('2d');

            new Chart(ctx, {
                type: 'line',
                data:{
                    labels: ['T1', 'T2', 'T3', 'T4', 'T5', 'T6', 'T7'],
                    datasets: [{
                        label: 'Error Trend',
                        data: data.error_trend,
                        borderColor: 'red'
                    }]
                }
            });
        }

        renderChart();

        setInterval(() => {
            location.reload();
        }, 5000);

      </script>

  </body>
</html>
"""

@app.route("/api/report")
def api_report():
    data = load_report()

    data["live_errors"]= live_data["errors"]
    data["error_trend"] = live_data["history"]

    return jsonify(data)

if __name__ == "__main__":
    threading.Thread(target=stream_logs, daemon=True).start()

    app.run(host="0.0.0.0", port=5000, debug=True)

