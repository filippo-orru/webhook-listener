# webhook-listener
Webserver that listens for (signed) Github webhooks and executes a script. Built using Docker &amp; Python.

## Usage
Create the webhook secret file:
```bash 
echo "mysecret" > webhook.secret
```

### Docker
```bash
docker build --tag webhook-listener .
docker run --rm -p 8080:8080 --name webhook-listener -v ./webhook.secret:/run/secrets/webhook_secret -e COMMAND="echo 'Hello World'" webhook-listener
```