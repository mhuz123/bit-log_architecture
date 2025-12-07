import time
import os

LOG_FILE = "/fluent-bit/logs/output.log"
INTERVAL = 10
SLEEP_TIME = 0.1

def monitor_throughput():
    total_logs = 0
    prev_size = 0
    last_check = time.time()

    print(f"Starting FluentBit throughput monitor (every {INTERVAL} seconds)...")
    print("Time | Logs in last interval | Total logs")

    while True:
        now = time.time()
        elapsed = now - last_check

        if elapsed >= INTERVAL:
            if not os.path.exists(LOG_FILE):
                print(f"Log file {LOG_FILE} does not exist yet")
                last_check = now
                continue

            current_size = os.path.getsize(LOG_FILE)

            # If file shrunk, assume it was rotated/truncated
            if current_size < prev_size:
                prev_size = 0

            new_lines = 0
            with open(LOG_FILE, "r") as f:
                if prev_size > 0:
                    f.seek(prev_size)
                new_lines = sum(1 for _ in f)

            prev_size = current_size
            total_logs += new_lines
            timestamp = time.strftime("%H:%M:%S")
            print(f"{timestamp} | last interval {new_lines} | total {total_logs}", flush=True)

            last_check = now

        time.sleep(SLEEP_TIME)

if __name__ == "__main__":
    monitor_throughput()
