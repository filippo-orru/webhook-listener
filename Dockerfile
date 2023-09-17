FROM python:3-slim

RUN apt update && apt install -y hugo

WORKDIR /app

COPY webhook-listener.py /app/webhook-listener.py

CMD ["python", "-u", "webhook-listener.py"]