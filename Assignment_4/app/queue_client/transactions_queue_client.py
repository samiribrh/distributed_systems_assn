import requests
from core.config import Config
import time

def fetch_batch_from_queue(batch_size):
    """
    Pull up to batch_size messages from the transactions queue.
    Blocks until at least one is available, then returns all available up to batch_size.
    """
    transactions = []
    # Block until at least one message is available
    while not transactions:
        url = f"{Config.QUEUE_API_BASE}/queues/{Config.TRANSACTIONS_QUEUE}/pull"
        try:
            resp = requests.get(url)
            if resp.status_code == 200:
                transactions.append(resp.json())
            else:
                # Queue empty, wait and retry
                time.sleep(0.5)
        except requests.RequestException as e:
            print(f"Error connecting to queue: {e}")
            time.sleep(1)
    # Now try to fetch up to batch_size-1 more (non-blocking)
    for _ in range(batch_size - 1):
        url = f"{Config.QUEUE_API_BASE}/queues/{Config.TRANSACTIONS_QUEUE}/pull"
        try:
            resp = requests.get(url)
            if resp.status_code == 200:
                transactions.append(resp.json())
            else:
                break  # No more messages right now
        except requests.RequestException as e:
            print(f"Error connecting to queue: {e}")
            break
    return transactions
