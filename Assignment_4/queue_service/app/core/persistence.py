import json
from threading import Timer
from app.core.config import Config
from app.core.logger import log_message
from app.core.storage import storage

def load_queues():
    """
    Loads queue data from disk and populates the in-memory storage.

    Attempts to read the queue data from the file specified by Config.STORAGE_PATH.
    If the file exists, loads the data into storage.queues.
    If the file does not exist, logs a message and starts with an empty set of queues.
    If another error occurs, logs the error message.
    """
    try:
        with open(Config.STORAGE_PATH, 'r') as f:
            storage.queues = json.load(f)
        log_message("Queues loaded from disk.")
    except FileNotFoundError:
        # This is not a fatal error; it just means there is no existing storage.
        log_message("Queue storage file not found, starting fresh.")
    except Exception as e:
        # Any other exception is logged for debugging purposes.
        log_message(f"Error loading queues: {e}")

def save_queues():
    """
    Saves the current in-memory queue data to disk.

    Dumps the storage.queues data as JSON into the file specified by Config.STORAGE_PATH.
    Logs a message upon successful save or logs an error if something goes wrong.
    """
    try:
        with open(Config.STORAGE_PATH, 'w') as f:
            json.dump(storage.queues, f)
        log_message("Queues saved to disk.")
    except Exception as e:
        # Log any exception that occurs during the save operation.
        log_message(f"Error saving queues: {e}")

def periodic_save():
    """
    Periodically persists the queue data to disk.

    This function is designed to be called repeatedly on a timer (interval defined by Config.PERSIST_INTERVAL).
    It calls save_queues() to save data, logs the completion, and sets up the next call using Timer.
    """
    save_queues()
    log_message("Periodic save completed.")
    # Schedule the next periodic save operation.
    Timer(Config.PERSIST_INTERVAL, periodic_save).start()
    