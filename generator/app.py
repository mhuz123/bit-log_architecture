from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
import time, json, random, os

app = FastAPI()


class TestConfig(BaseModel):
    rate: float = 10
    mode: str = "steady"
    duration: int = 60


def generate_logs(rate, mode, duration):
    start_time = time.time()
    last_sec_time = start_time
    logs_per_sec = []
    logs_this_second = 0

    os.makedirs("/app/logs", exist_ok=True)
    os.makedirs("/app/stats", exist_ok=True)

    with open("/app/logs/log.txt", "a") as logs:
        while True:
            now = time.time()
            elapsed = now - start_time

            if elapsed > duration:
                if logs_this_second > 0:
                    logs_per_sec.append(logs_this_second)

                    print(f"{time.strftime('%H:%M:%S')} | {logs_this_second}", flush=True)
                break

            if mode == "burst":
                count = int(rate * 5)
            elif mode == "steady":
                count = 1
            elif mode == "randomized":
                count = max(1, int(random.uniform(0.5 * rate, 2 * rate)))
            elif mode == "peak_idle":
                current_time = int(elapsed) % 10
                current_rate = rate * 5 if current_time < 5 else rate * 0.2
                count = max(1, int(current_rate))
            else:
                count = 1

            for _ in range(count):
                entry = {
                    "timestamp": time.time(),
                    "level": random.choice(["INFO", "WARN", "ERROR"]),
                    "message": "Synthetic log event",
                    "value": random.randint(1, 100)
                }

                line = json.dumps(entry)
                logs.write(line + "\n")
                logs.flush()
                logs_this_second += 1

            if now - last_sec_time >= 1.0:
                logs_per_sec.append(logs_this_second)
                print(f"{time.strftime('%H:%M:%S')} | {logs_this_second}", flush=True)
                logs_this_second = 0
                last_sec_time = now

            time.sleep(1 / max(rate, 0.01))

    total_logs = sum(logs_per_sec)
    avg_logs = total_logs / len(logs_per_sec) if logs_per_sec else 0
    max_logs = max(logs_per_sec) if logs_per_sec else 0
    min_logs = min(logs_per_sec) if logs_per_sec else 0

    stats = {
        "rate": rate,
        "mode": mode,
        "duration": duration,
        "start_time": start_time,
        "total_logs": total_logs,
        "avg_logs_per_sec": avg_logs,
        "max_logs_per_sec": max_logs,
        "min_logs_per_sec": min_logs,
        "logs_each_second": logs_per_sec
    }

    start_str = str(int(start_time))
    stats_filename = f"/app/stats/stats{rate}{mode}{duration}-{start_str}.json"

    with open(stats_filename, "w") as f:
        json.dump(stats, f, indent=4)

    console_stats = stats.copy()
    console_stats.pop("logs_each_second", None)
    print("\n--- FINAL STATS ---", flush=True)
    print(json.dumps(console_stats, indent=4), flush=True)


@app.post("/start-test")
def start_test(config: TestConfig, background_tasks: BackgroundTasks):
    background_tasks.add_task(generate_logs, config.rate, config.mode, config.duration)

    return {
        "status": "started",
        "config": config
    }
