import json
from threading import Timer
from app.core.config import Config
from app.core.logger import log_message
from app.core.storage import storage

def load_queues():
    try:
        with open(Config.STORAGE_PATH, 'r') as f:
            storage.queues = json.load(f)
        log_message("Queues loaded from disk.")
    except FileNotFoundError:
        log_message("Queue storage file not found, starting fresh.")
    except Exception as e:
        log_message(f"Error loading queues: {e}")

def save_queues():
    try:
        with open(Config.STORAGE_PATH, 'w') as f:
            json.dump(storage.queues, f)
        log_message("Queues saved to disk.")
    except Exception as e:
        log_message(f"Error saving queues: {e}")

def periodic_save():
    save_queues()
    log_message("Periodic save completed.")
    Timer(Config.PERSIST_INTERVAL, periodic_save).start()
