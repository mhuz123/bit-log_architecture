FROM python:3.12-slim

WORKDIR /app

COPY cpu-monitor.py .

RUN pip install --upgrade pip && pip install docker

CMD ["python", "cpu-monitor.py"]
