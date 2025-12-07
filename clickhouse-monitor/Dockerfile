FROM python:3.12-slim

WORKDIR /app

# Install ClickHouse client
RUN pip install clickhouse-connect

# Copy the script
COPY clickhouse-monitor.py /app/clickhouse-monitor.py

# Run the monitor
CMD ["python", "-u", "/app/clickhouse-monitor.py"]
