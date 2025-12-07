FROM python:3.12-slim

WORKDIR /app

RUN pip install --upgrade pip && pip install clickhouse-connect

COPY clickhouse-monitor.py /app/clickhouse-monitor.py

CMD ["python", "-u", "/app/clickhouse-monitor.py"]
