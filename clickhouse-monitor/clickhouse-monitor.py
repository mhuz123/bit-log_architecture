import time
import sys
from clickhouse_connect import get_client, driver
sys.stdout.reconfigure(line_buffering=True)

# Config
CLICKHOUSE_HOST = 'clickhouse'
CLICKHOUSE_PORT = 8123
CLICKHOUSE_USER = 'clickhouse'
CLICKHOUSE_PASSWORD = 'clickhouse'
TABLE = 'logs'
INTERVAL = 10        # seconds
SLEEP_TIME = 0.1     # seconds between time checks
RETRY_INTERVAL = 5

def connect():
    while True:
        try:
            client = get_client(
                host=CLICKHOUSE_HOST,
                port=CLICKHOUSE_PORT,
                username=CLICKHOUSE_USER,
                password=CLICKHOUSE_PASSWORD
            )
            client.query("SELECT 1")
            print("Connected to ClickHouse successfully.")
            return client
        except driver.exceptions.OperationalError as e:
            print(f"ClickHouse connection failed: {e}. Retrying in {RETRY_INTERVAL} seconds...")
            time.sleep(RETRY_INTERVAL)

def get_rows(client):
    try:
        result = client.query(f"SELECT count() FROM {TABLE}")
        return int(result.result_rows[0][0])
    except Exception as e:
        print(f"Error fetching row count: {e}")
        return None

def print_latency(client):
    try:
        query = """
                SELECT avg(dateDiff('millisecond', timestamp, received_at)) AS avg_latency_ms, \
                       max(dateDiff('millisecond', timestamp, received_at)) AS max_latency_ms, \
                       min(dateDiff('millisecond', timestamp, received_at)) AS min_latency_ms
                FROM logs
                WHERE timestamp >= now() - INTERVAL 10 SECOND
                """
        result = client.query(query)
        avg_latency = result.result_rows[0][0]
        max_latency = result.result_rows[0][1]
        min_latency = result.result_rows[0][2]

        print(f"{time.strftime('%H:%M:%S')} | LATENCY | Avg: {avg_latency:.2f} ms | "
              f"Max: {max_latency:.2f} ms | Min: {min_latency:.2f} ms")

    except Exception as e:
        print(f"Error fetching latency: {e}")

if __name__ == "__main__":
    client = connect()
    prev_rows = get_rows(client) or 0
    total_rows = prev_rows

    print(f"Monitoring ClickHouse table '{TABLE}' every {INTERVAL} second(s)...")
    print("Time | Rows in last interval | Total rows so far")

    prev_time = time.time()

    while True:
        cur_time = time.time()
        elapsed = cur_time - prev_time

        if elapsed >= INTERVAL:
            cur_rows = get_rows(client)
            if cur_rows is None:
                client = connect()
                cur_rows = get_rows(client) or prev_rows

            diff = cur_rows - prev_rows
            total_rows += diff
            timestamp = time.strftime('%H:%M:%S')

            print(f"{timestamp} | THROUGHPUT | last interval {diff} | total {total_rows}", flush=True)

            prev_rows = cur_rows
            prev_time = cur_time

            print_latency(client)

        time.sleep(SLEEP_TIME)
