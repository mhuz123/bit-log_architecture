import time
import json
import random


def generate_logs(rate=10):
    with open("/app/logs/log.txt", "a") as logs:
        while True:
            entry = {
                "timestamp": time.time(),
                "level": random.choice(["INFO", "WARN", "ERROR"]),
                "message": "Synthetic log event",
                "value": random.randint(1,100)
            }
            logs.write(json.dumps(entry) + "\n")
            logs.flush()
            time.sleep(1 / rate)

if __name__ == "__main__":
    generate_logs(1)

