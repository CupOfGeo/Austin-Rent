import socketserver
from http.server import BaseHTTPRequestHandler

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
            logger.error(f"{self.address_string()} - GET {self.path} 404")


def run_simple_webserver():
    # port = int(os.environ.get("PORT", 8080))
    logger.info("Starting health check server", port=8080)
    with socketserver.TCPServer(("", 8080), HealthRequestHandler) as httpd:
        httpd.serve_forever()
