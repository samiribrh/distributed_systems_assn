from app.core.config import Config
from app.core.storage import storage
from app.core.logger import log_message

def initialize_default_queues():
    """
    Creates default queues on service startup if they do not already exist.

    This function iterates over the list of queue names defined in Config.DEFAULT_QUEUES.
    For each queue name, it checks if the queue is already present in storage.
    If the queue does not exist, it initializes the queue as an empty message list and logs the creation.
    """
    for queue_name in Config.DEFAULT_QUEUES:
        if queue_name not in storage.get_queues():
            storage.get_queues()[queue_name] = {"messages": []}
            log_message(f"Automatically created queue: {queue_name}")
