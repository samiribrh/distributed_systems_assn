import os
from pathlib import Path

class Config:
    NUM_WORKERS = int(os.getenv("NUM_WORKERS", 5))  # number of workers
    QUEUE_SERVICE_HOST = os.getenv("QUEUE_SERVICE_HOST", "queue_service")  # host for queue service
    QUEUE_SERVICE_PORT = int(os.getenv("QUEUE_SERVICE_PORT", 7500))  # port for queue service
    QUEUE_API_BASE = f"http://{QUEUE_SERVICE_HOST}:{QUEUE_SERVICE_PORT}/api/v1"  # api base url
    TRANSACTIONS_QUEUE = os.getenv("TRANSACTIONS_QUEUE", "transactions")  # queue name for transactions
    RESULTS_QUEUE = os.getenv("RESULTS_QUEUE", "results")  # queue name for results
    MODEL_PATH = str(Path(__file__).parent.parent / "models" / "fraud_rf_model.pkl")  # path where model is located
    FETCH_SLEEP_TIME = 5  # seconds after each fetch
