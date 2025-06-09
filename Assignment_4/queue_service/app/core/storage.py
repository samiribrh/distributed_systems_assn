from threading import Lock

class QueueStorage:
    """
    Thread-safe singleton class for managing in-memory queue storage.

    This class ensures that only one instance exists throughout the application,
    and provides methods to access and update the in-memory queues dictionary.
    """
    _instance = None  # Holds the singleton instance
    _lock = Lock()    # Lock for thread-safe singleton initialization

    def __new__(cls):
        """
        Implements the singleton pattern with thread safety.

        If no instance exists, acquires a lock and creates one.
        Returns the singleton instance on every call.
        """
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:  # Double-checked locking
                    cls._instance = super().__new__(cls)
                    # Initialize the queues dictionary on first creation
                    cls._instance.queues = {}
        return cls._instance

    def update(self, data):
        """
        Updates the internal queues dictionary with new data.

        Args:
            data (dict): A dictionary containing queue data to merge into storage.
        """
        self.queues.update(data)

    def get_queues(self):
        """
        Returns the internal queues dictionary.

        Returns:
            dict: The dictionary containing all queues.
        """
        return self.queues

# Singleton instance of QueueStorage used throughout the application.
storage = QueueStorage()
