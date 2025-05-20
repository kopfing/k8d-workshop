import os
import signal
import socket
import sys
from flask import Flask, jsonify, send_from_directory
from datetime import datetime, timezone
import argparse


APP_VERSION = "1.0.2"

app = Flask(__name__, static_folder="static")

@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/api/info")
def info():
    return jsonify({
        "timestamp": datetime.now(timezone.utc).isoformat() + "Z",
        "hostname": socket.gethostname(),
        "version": APP_VERSION
    })

def graceful_exit(signum, frame):
    print(f"Received signal {signum}, shutting down gracefully...")
    sys.exit(0)

if __name__ == "__main__":
    print(f"App version: {APP_VERSION}")
    # Register signal handlers
    signal.signal(signal.SIGINT, graceful_exit)   # Ctrl+C
    signal.signal(signal.SIGTERM, graceful_exit)  # docker stop, kill -15
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true', help='Enable Flask debug mode (hot reloading)')
    args = parser.parse_args()
    app.run(debug=args.debug, host="0.0.0.0", port=3000)
