FROM python:3.12-slim

WORKDIR /app

# Install ClickHouse client
RUN pip install clickhouse-connect

# Copy the script
COPY clickhouse-throughput-monitor.py /app/clickhouse-throughput-monitor.py

# Run the monitor
CMD ["python", "-u", "/app/clickhouse-throughput-monitor.py"]
