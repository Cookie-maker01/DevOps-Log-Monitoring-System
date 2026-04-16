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
    <html>
    <head>
        <title>DevOps Dashboard</title>
        <style>
            body { font-family: Arial; margin: 40px; }
            .card { padding: 20px; margin: 10px; background: #f4f4f4; }
        </style>
    </head>

    <body>
        <h1>DevOpes Log Dashboard</h1>

        <div class="card">
            <p>Open API: <a href="/api/report">/api/report</a></p>
        </div>
      </body>
      </html>
      """

@app.route("/api/report")
def api_report():
    return jsonify(load_report())

if __name__ == "__main__":
    app.run(debug=True)

