import time
import random
from datetime import datetime

LOG_FILE = "logs/app.log"

levels = ["INFO", "WARN", "ERROR"]
endpoints = [
  "/api/users",
  "/api/login",
  "/api/orders",
  "/api/payments"
]

status_codes = [200, 200, 200, 404, 500, 502]

def generate_log():
    
    timestamp = datetime.now().isoformat()

    level = random.choices(levels, weights=[6, 2, 2])[0]
    endpoint = random.choice(endpoints)
    status = random.choice(status_codes)
    response_time = random.randint(50, 500)

    log = f"{timestamp} {level} GET {endpoint} {status} {response_time}ms"

    return log

if __name__ == "__main__":
    
    print("Log generator started...")

    while True:
        
        log = generate_log()

        with open(LOG_FILE, "a") as f:
            f.write(log + "\n")

        print(log)

        time.sleep(2)