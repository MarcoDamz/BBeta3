#!/usr/bin/env python3
"""
Worker wrapper with HTTP health check for Cloud Run.
Runs both a Celery worker and a simple health check server.
"""
import os
import sys
import subprocess
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler


class HealthCheckHandler(BaseHTTPRequestHandler):
    """Simple HTTP handler for health checks."""

    def do_GET(self):
        """Handle GET requests - always return 200 OK."""
        if self.path == "/" or self.path == "/health":
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(b"OK - Celery Worker Running")
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        """Suppress default logging."""
        pass  # Comment this out to enable access logs


def run_health_server(port=8080):
    """Run the health check HTTP server."""
    server = HTTPServer(("0.0.0.0", port), HealthCheckHandler)
    print(f"✓ Health check server started on port {port}")
    server.serve_forever()


def run_celery_worker():
    """Run the Celery worker process."""
    cmd = [
        "celery",
        "-A",
        "chatagentb",
        "worker",
        "--loglevel=info",
        "--concurrency=2",
        "--max-tasks-per-child=1000",
    ]

    print(f"✓ Starting Celery worker: {' '.join(cmd)}")

    # Run celery worker and wait for it
    process = subprocess.Popen(cmd)
    process.wait()

    # If worker exits, exit with same code
    sys.exit(process.returncode)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8080"))

    print("=" * 60)
    print("🚀 Starting ChatAgentB Celery Worker with Health Check")
    print("=" * 60)

    # Start health check server in background thread
    health_thread = threading.Thread(
        target=run_health_server, args=(port,), daemon=True
    )
    health_thread.start()

    # Run Celery worker in main thread (blocks)
    run_celery_worker()
