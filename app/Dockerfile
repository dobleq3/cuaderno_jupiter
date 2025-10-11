FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
COPY app.py .
COPY wait-for-it.sh .

# Instala dependencias del sistema y zabbix-sender
RUN apt-get update && apt-get install -y gcc libpq-dev zabbix-sender && \
    pip install --no-cache-dir -r requirements.txt && \
    chmod +x /app/wait-for-it.sh

EXPOSE 5000

CMD ["./wait-for-it.sh", "db:5432", "--", "python", "app.py"]
