import time

LOG_FILE = "logs/app.log"

def follow(file):

    file.seek(0, 2)

    while True:
        
        line = file.readline()

        if not line:
            time.sleep(1)
            continue
        
        yield line

def process_log(line):
    
    parts = line.strip().split()

    if len(parts) < 6:
        return
    
    level = parts[1]
    endpoint = parts[3]

    print(f"Streaming Log → {level} {endpoint}")

    if level == "ERROR":
        print("ALERT: Error detected!")


if __name__ == "__main__":
    
    print("Streaming analyzer started...")

    with open(LOG_FILE, "r") as f:
        
        for line in follow(f):
            
            process_log(line)