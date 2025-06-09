class Config:
    MAX_QUEUE_SIZE = 10  # max size for a queue
    PERSIST_INTERVAL = 5  # seconds
    STORAGE_PATH = 'data/queues.json'  # path for storage of queues
    LOG_PATH = 'logs/queue_service.log'  # path for log file
    DEFAULT_QUEUES = ["results", "transactions"]  # queues that will be created automatically on startup
