from http.server import BaseHTTPRequestHandler, HTTPServer
import subprocess
import os
import hmac
import hashlib
import sys
import signal
from datetime import datetime
import shlex

PORT: int = int(os.getenv('PORT') or 8080)
PRINT_DEMO_SIGNATURE: bool = os.getenv('PRINT_DEMO_SIGNATURE') == 'true'
COMMAND = os.getenv('COMMAND')
WEBHOOK_SECRET_PATH = os.getenv('WEBHOOK_SECRET_PATH') or "/run/secrets/webhook_secret"

webhook_secret = ""
web_server: HTTPServer = None

class WebhookListener(BaseHTTPRequestHandler):
    def do_POST(self):
        global webhook_secret
        if self.path == '/webhook':
            signature = self.headers.get('X-Hub-Signature')
            if not signature:
                self.send_error(400, 'X-Hub-Signature header missing')
                return

            request_body = self.rfile.read(int(self.headers.get('Content-Length')))
            sha1 = hmac.new(webhook_secret.encode(), request_body, hashlib.sha1)
            if not hmac.compare_digest('sha1=' + sha1.hexdigest(), signature):
                self.send_error(401, 'X-Hub-Signature verification failed')
                print('X-Hub-Signature verification failed. Expected %s, got %s' % (signature, sha1.hexdigest()))
                return

            print("Executing command...\n>%s" % COMMAND)
            self.send_response(200)
            self.send_header('Content-type', 'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write(b'OK\n')
            self.wfile.flush()

            subprocess.Popen(["sh", "-c", "\"%s\"" % COMMAND], stdout=sys.stdout, stderr=sys.stderr)
        else:
            self.send_error(404, 'Not found')

def terminate(signal,frame):
  print("Terminating at %s ..." % datetime.now())
  web_server.server_close()
  sys.exit(0)


def run():
    global web_server
    global webhook_secret
    
    with open(WEBHOOK_SECRET_PATH, 'r') as f:
        webhook_secret = f.read().strip()
        if not webhook_secret:
            print('Webhook secret file is empty')
            return
    

    if PRINT_DEMO_SIGNATURE:
        demoBody = '{"ref":"refs/heads/master"}'
        print('Demo signature for body %s = "%s"' % 
            (demoBody, hmac.new(webhook_secret.encode(), demoBody.encode(), hashlib.sha1).hexdigest()))
    
    server_address = ('', PORT)
    web_server = HTTPServer(server_address, WebhookListener)
    print('Starting webhook listener...')
    web_server.serve_forever()

if __name__ == '__main__':
    signal.signal(signal.SIGTERM, terminate)
    run()
