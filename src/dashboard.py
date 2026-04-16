from flask import Flask, jsonify
import json

app = Flask(__name__)

def load_report():
    try:
        with open("reports/report.json", "r") as f:
            return json.load(f)
    except:
        return {}
    
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

    data["error_trend"] = [0, 1 , 0, 2, 1, 3, 2]
    return jsonify(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

