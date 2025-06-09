from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
from app.api.v1.endpoints.queue import router as queue_router
from app.core.persistence import load_queues, periodic_save, save_queues
from app.core.logger import log_message
from app.core.queue_initializer import initialize_default_queues
import signal
import sys

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    FastAPI lifespan context manager.

    This function runs at application startup before the server begins accepting requests.
    It is used to perform setup tasks such as creating default queues.
    """
    # Initialize default queues on service startup
    initialize_default_queues()
    yield
    # Additional cleanup tasks could be added here if needed

# Create the FastAPI application instance, using the custom lifespan handler
app = FastAPI(lifespan=lifespan)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    """
    Middleware for logging all incoming HTTP requests and their responses.

    Logs the client IP, request method, URL, and headers before processing,
    and logs the response status code after processing.
    """
    client_ip = request.client.host
    method = request.method
    url = request.url.path
    headers = dict(request.headers)

    log_message(f"Request from {client_ip} - {method} {url} - Headers: {headers}")
    response = await call_next(request)
    log_message(f"Response to {client_ip} - Status: {response.status_code}")
    return response

# Load queues from persistent storage at application startup
load_queues()

# Start periodic saving of the queues to disk at fixed intervals
periodic_save()

# Register the API routes for queue operations, with prefix '/api/v1'
app.include_router(queue_router, prefix='/api/v1')

def shutdown_handler(sig, frame):
    """
    Signal handler for graceful application shutdown.

    This function is called when the application receives a SIGINT or SIGTERM signal.
    It saves the current queue data to disk, logs the shutdown, and exits.
    """
    save_queues()
    log_message("Gracefully shutting down the message queue service.")
    sys.exit(0)

# Register signal handlers for graceful shutdown on SIGINT and SIGTERM
signal.signal(signal.SIGINT, shutdown_handler)
signal.signal(signal.SIGTERM, shutdown_handler)
