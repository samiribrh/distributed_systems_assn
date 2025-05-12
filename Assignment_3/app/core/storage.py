from threading import Lock

class QueueStorage:
    _instance = None
    _lock = Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance.queues = {}
        return cls._instance

    def update(self, data):
        self.queues.update(data)

    def get_queues(self):
        return self.queues

storage = QueueStorage()
