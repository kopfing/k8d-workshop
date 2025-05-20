import os
import socket
import signal
import sys
import time
from flask import Flask, jsonify, send_from_directory, Response
from datetime import datetime, timezone
import psycopg2
from psycopg2.extras import RealDictCursor
import argparse

APP_VERSION = "2.1.0"
DB_PARAMS = {
    'host': os.environ.get('POSTGRES_HOST', 'db'),
    'port': os.environ.get('POSTGRES_PORT', 5432),
    'dbname': os.environ.get('POSTGRES_DB', 'demo'),
    'user': os.environ.get('POSTGRES_USER', 'demo'),
    'password': os.environ.get('POSTGRES_PASSWORD', 'demo'),
}

app = Flask(__name__, static_folder="static")
conn = None
STARTUP_TIME = time.time()
STARTUP_DELAY = 5  # seconds
READINESS_DELAY = 2  # seconds

# Add a global flag to force healthz failure
force_healthz_fail = False

BG_COLOR = os.environ.get('BG_COLOR', '#fff')
TITLE_SUFFIX = os.environ.get('TITLE_SUFFIX', '')

def get_db_conn():
    global conn
    if conn is None or conn.closed:
        try:
            conn = psycopg2.connect(**DB_PARAMS)
        except Exception:
            conn = None
    return conn

def try_creating_table():
    db = get_db_conn()
    if db is None:
        return
    with db.cursor() as cur:
        cur.execute('''
            CREATE TABLE IF NOT EXISTS requests (
                id SERIAL PRIMARY KEY,
                timestamp TIMESTAMPTZ NOT NULL,
                hostname TEXT NOT NULL,
                version TEXT NOT NULL
            )
        ''')
        db.commit()

def graceful_exit(signum, frame):
    print(f"Received signal {signum}, shutting down gracefully...")
    if conn:
        conn.close()
    sys.exit(0)


@app.route("/")
def index():
    try:
        with open(os.path.join(app.static_folder, "index.html")) as f:
            html = f.read()
        # Inject background color style into <body>
        html = html.replace('<body>', f'<body style="background-color: {BG_COLOR};">')
        # Inject title suffix into <h1>
        if TITLE_SUFFIX:
            html = html.replace('<h1>K8s Workshop Demo App v2</h1>', f'<h1>K8s Workshop Demo App v2 {TITLE_SUFFIX}</h1>')
        return Response(html, mimetype='text/html')
    except Exception as e:
        return f"Error loading page: {e}", 500

@app.route("/api/info")
def info():
    db = get_db_conn()
    if db is None:
        return jsonify({"error": "Database unavailable"}), 503
    # Try to ensure table if DB is available, but don't block if db is not available
    try:
        # NOTE: In production code, DB schema changes should (migrations) should be handled outside the app livecycle
        try_creating_table()
    except Exception:
        return jsonify({"error": "Table creation failed"}), 503
    now = datetime.now(timezone.utc)
    hostname = socket.gethostname()
    with db.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(
            "INSERT INTO requests (timestamp, hostname, version) VALUES (%s, %s, %s)",
            (now, hostname, APP_VERSION)
        )
        db.commit()
        cur.execute(
            "SELECT * FROM requests ORDER BY id DESC LIMIT 10"
        )
        records = cur.fetchall()[::-1]  # oldest first
        if len(records) > 1:
            t0 = records[0]['timestamp']
            tN = records[-1]['timestamp']
            seconds = (tN - t0).total_seconds() or 1
            avg_req_per_sec = (len(records)-1) / seconds
        else:
            avg_req_per_sec = 0.0
    return jsonify({
        "timestamp": now.isoformat() + "Z",
        "hostname": hostname,
        "version": APP_VERSION,
        "last_10_records": records,
        "avg_req_per_sec": avg_req_per_sec
    })

@app.route("/healthz")
def healthz():
    global force_healthz_fail
    if force_healthz_fail:
        return jsonify({"status": "forced failure"}), 503
    if time.time() - STARTUP_TIME < STARTUP_DELAY:
        return jsonify({"status": "starting"}), 503
    return jsonify({"status": "ok"}), 200

@app.route("/api/fail-healthz")
def fail_healthz():
    global force_healthz_fail
    force_healthz_fail = True
    return jsonify({"status": "healthz will now fail"}), 200

@app.route("/readyz")
def readyz():
    if force_healthz_fail:
        return jsonify({"status": "forced failure"}), 503
    if time.time() - STARTUP_TIME < (STARTUP_DELAY + READINESS_DELAY):
        return jsonify({"status": "starting"}), 503
    db = get_db_conn()
    if db is None:
        return jsonify({"status": "not ready", "reason": "db unavailable"}), 503
    try:
        with db.cursor() as cur:
            cur.execute("SELECT 1")
        return jsonify({"status": "ready"}), 200
    except Exception:
        return jsonify({"status": "not ready", "reason": "db error"}), 503

def main():
    print(f"App version: {APP_VERSION}", flush=True)
    # Register signal handlers
    signal.signal(signal.SIGINT, graceful_exit)   # Ctrl+C
    signal.signal(signal.SIGTERM, graceful_exit)  # docker stop, kill -15
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true', help='Enable Flask debug mode (hot reloading)')
    args = parser.parse_args()
    app.run(debug=args.debug, host="0.0.0.0", port=3000)

if __name__ == "__main__":
    main()
