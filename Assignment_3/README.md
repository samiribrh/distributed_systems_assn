# Message Queue Service

## Introduction

The Message Queue Service is designed to facilitate high-performance computing (HPC) tasks by implementing a queue system for managing message transactions. It supports queue creation, deletion, message pushing, and pulling via a RESTful API built with FastAPI. The service is designed to handle message persistence, periodic saving, and graceful shutdown.

## Features

* Queue Management: Create, delete, list queues.
* Message Handling: Push and pull messages from a queue.
* Persistent Storage: Saves queues periodically to a file.
* Graceful Shutdown: Saves data on shutdown to prevent loss.
* Logging: Logs every client request and server response.
* Configurable: Easily adjustable queue size limit and save interval.

## Installation

### Prerequisites

* Python 3.12+
* Poetry for dependency management

## Configuration

Configuration file is located at `app/core/config.py`.

### Example Configuration

```python
class Config:
    MAX_QUEUE_SIZE = 100    # Maximum number of messages per queue
    PERSIST_INTERVAL = 3    # Time interval (seconds) for saving queues
    STORAGE_PATH = 'data/queues.json'
    LOG_PATH = 'logs/queue_service.log'
```

## Running the Service

Start the server using Uvicorn:

```bash
poetry run uvicorn app.main:app --host 0.0.0.0 --port 7500
```

## API Endpoints

### Queue Management

* **Create Queue:** POST `/api/v1/queues` - `{ "queue_name": "test_queue" }`
* **List Queues:** GET `/api/v1/queues`
* **Delete Queue:** DELETE `/api/v1/queues/{queue_name}`

### Message Operations

* **Push Message:** POST `/api/v1/queues/{queue_name}/push` - `{ "transaction_id": "12345", "data": { "key": "value" } }`
* **Pull Message:** GET `/api/v1/queues/{queue_name}/pull`

## Logging

Logs are stored in the `logs/queue_service.log` file. Each request and response is logged with:

* Timestamp
* Request Method
* URL
* Client IP
* Status Code
* Response Message

## Testing

Run the test script to verify functionality:

```bash
python3 test.py
```

## Error Handling

* Queue not found: Returns 404
* Queue full: Returns 400
* Empty queue on pull: Returns 404
