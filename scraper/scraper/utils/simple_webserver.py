import socketserver
from http.server import BaseHTTPRequestHandler

import structlog

from scraper.config.settings import settings

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
    PORT = settings.webserver_port
    logger.info("Starting health check server", port=PORT)
    with socketserver.TCPServer(("", PORT), HealthRequestHandler) as httpd:
        httpd.serve_forever()
