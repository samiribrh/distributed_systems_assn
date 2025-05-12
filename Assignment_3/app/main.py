from fastapi import FastAPI, Request
from app.api.v1.endpoints.queue import router as queue_router
from app.core.persistence import load_queues, periodic_save, save_queues
from app.core.logger import log_message
from app.core.storage import storage
import signal
import sys

app = FastAPI()

@app.middleware("http")
async def log_requests(request: Request, call_next):
    client_ip = request.client.host
    method = request.method
    url = request.url.path
    headers = dict(request.headers)

    log_message(f"Request from {client_ip} - {method} {url} - Headers: {headers}")
    response = await call_next(request)
    log_message(f"Response to {client_ip} - Status: {response.status_code}")
    return response

load_queues()

periodic_save()

app.include_router(queue_router, prefix='/api/v1')

def shutdown_handler(sig, frame):
    save_queues()
    log_message("Gracefully shutting down the message queue service.")
    sys.exit(0)

signal.signal(signal.SIGINT, shutdown_handler)
signal.signal(signal.SIGTERM, shutdown_handler)
