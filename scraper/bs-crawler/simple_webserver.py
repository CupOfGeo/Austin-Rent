import os
from http.server import BaseHTTPRequestHandler, HTTPServer
import structlog

logger = structlog.get_logger()

class HealthRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
        else:
            self.send_response(404)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            # self.wfile.write(b"Not Found")
            logger.error(f"{self.address_string()} - GET {self.path} 404")

def run_simple_webserver(server_class: HTTPServer, handler_class: HealthRequestHandler):
    port = int(os.environ.get("PORT", 8080))
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logger.info(f"Starting server on port {port}")
    httpd.serve_forever()