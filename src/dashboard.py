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
    print("ERROR COUNT:", live_data["errors"])

    with open(LOG_FILE, "r") as f:

        while True:
            line = f.readline()

            if not line:
                time.sleep(1)
                continue

            print("LINE:", line.strip())

            parts = line.strip().split()

            if "ERROR" in parts:
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
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>

<body>
    <h1>DevOps Log Dashboard</h1>

    <canvas id="errorChart" width="400" height="200"></canvas>

    <script>

        let chart;

        async function loadData() {
            const res = await fetch('/api/report');
            return await res.json();
        }

        function initChart() {
        
            const ctx = document.getElementById('errorChart').getContext('2d');

            chart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: [],
                    datasets: [{
                        label: 'Errors',
                        data:[],
                        borderColor: 'red'
                    }]
                }
            });
        }

        async function updateChart() {

            const res = await fetch('/api/report');
            const data = await res.json();

            console.log("API DATA:", data);

            chart.data.labels = data.history.map((_, i) => i);
            chart.data.datasets[0].data = data.history;

            chart.update();
        }

        initChart();

        setInterval(updateChart, 2000);

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

    app.run(host="0.0.0.0", port=5000, debug=False)

