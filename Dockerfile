FROM python:3-slim

RUN apt update && apt install -y curl git

ARG PRE_BUILD_COMMAND="echo 'No pre-build command specified'"
RUN eval ${PRE_BUILD_COMMAND}

WORKDIR /app
ADD --chmod=600 shared/ssh/* /root/.ssh/

RUN ssh-keyscan -t rsa github.com > /root/.ssh/known_hosts

COPY webhook-listener.py webhook-listener.py

CMD ["python", "-u", "webhook-listener.py"]