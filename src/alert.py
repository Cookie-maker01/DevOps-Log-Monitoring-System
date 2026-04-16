import requests
import json

SLACK_WEBHOOK = "YOUR_WEBHOOK_URL"

def send_slack_alert(message):

    payload = {
        "text": message
    }

    requests.post(
        SLACK_WEBHOOK,
        data=json.dumps(payload),
        headers={"Content-Type": "application/json"}
    )