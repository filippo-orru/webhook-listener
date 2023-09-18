FROM python:3-slim

RUN apt update && apt install -y hugo

USER root:root
WORKDIR /root
ADD --chmod=600 --chown="root:root" shared/ssh/* /root/.ssh/

COPY webhook-listener.py webhook-listener.py

CMD ["python", "-u", "webhook-listener.py"]