FROM python:3-slim

RUN apt update && apt install -y hugo

WORKDIR /app

COPY shared/ssh/ /root/.ssh/
RUN chmod 600 /root/.ssh/*
RUN chown root:root /root/.ssh/*

COPY webhook-listener.py /app/webhook-listener.py

CMD ["python", "-u", "webhook-listener.py"]