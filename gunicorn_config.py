# Gunicorn configuration for WeWorkLocal
# Save this file as: /home/weworklocal/weworklocal/gunicorn_config.py

import multiprocessing
import os

# Server socket
bind = "unix:/home/weworklocal/weworklocal/gunicorn.sock"
backlog = 2048

# Worker processes
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2

# Restart workers after this many requests, to help prevent memory leaks
max_requests = 1000
max_requests_jitter = 50

# Logging
accesslog = "/home/weworklocal/logs/gunicorn_access.log"
errorlog = "/home/weworklocal/logs/gunicorn_error.log"
loglevel = "info"

# Process naming
proc_name = "weworklocal"

# Server mechanics
daemon = False
pidfile = "/home/weworklocal/weworklocal/gunicorn.pid"
user = "weworklocal"
group = "weworklocal"
tmp_upload_dir = None

# SSL (if needed)
# keyfile = "/path/to/keyfile"
# certfile = "/path/to/certfile"

# Environment
raw_env = [
    "DJANGO_SETTINGS_MODULE=weworklocal.production_settings",
]

# Preload application for better performance
preload_app = True

# Worker process lifecycle
def when_ready(server):
    server.log.info("Server is ready. Spawning workers")

def worker_int(worker):
    worker.log.info("worker received INT or QUIT signal")

def pre_fork(server, worker):
    server.log.info("Worker spawned (pid: %s)", worker.pid)

def post_fork(server, worker):
    server.log.info("Worker spawned (pid: %s)", worker.pid)

def post_worker_init(worker):
    worker.log.info("Worker initialized (pid: %s)", worker.pid)

def worker_abort(worker):
    worker.log.info("Worker aborted (pid: %s)", worker.pid)
