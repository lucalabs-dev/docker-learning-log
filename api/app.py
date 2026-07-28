import shutil

from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):

        if self.path == "/api/log":

            with open("data/learning_logs/test_log.txt", "r") as file:
                logs = file.read()

            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()

            self.wfile.write(logs.encode())

        else:

            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"API funktioniert")
    def do_POST(self):
        length = int(self.headers["Content-Length"])
        data = self.rfile.read(length).decode()

        parsed_data = parse_qs(data)

        if "text" in parsed_data:
            log_entry = parsed_data["text"][0]
            add_to_log(log_entry)

        self.send_response(302)
        self.send_header("Location", "/")
        self.end_headers()

def add_to_log(log_entry):
    with open("data/learning_logs/test_log.txt", "a") as file:
        file.write("\n\n" + log_entry)

    create_backup()

def create_backup():
    date = datetime.now().strftime("%Y-%m-%d_%H-%M")
    backup_path = "data/learning_logs/backups/test-log_backup_" + date + ".txt"
    shutil.copy("data/learning_logs/test_log.txt", backup_path)

        
server = HTTPServer(("0.0.0.0", 3000), Handler)
print("API läuft auf Port 3000")
server.serve_forever()