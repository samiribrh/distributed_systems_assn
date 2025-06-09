# Distributed Systems Assignment 4: High Performance Computing

## Overview

This project implements a distributed fraud detection system using a message queue microservice (`queue_service`) and a high-performance machine learning prediction service (`mpi_prediction`) powered by MPI (Message Passing Interface).

- **queue_service**: RESTful service to create, push, pull, list, and delete message queues (used for transactions and results).
- **mpi_prediction**: Distributed ML prediction service that fetches transactions, distributes predictions across worker processes (using MPI), and posts results.


## File Structure

Assignment_4/
├── queue_service/
│ ├── app/
│ │ ├── api/
│ │ │ └── v1/
│ │ │ └── queues.py # API endpoints for queues
│ │ ├── core/
│ │ │ ├── config.py # Configurations
│ │ │ ├── logger.py # Logging utility
│ │ │ ├── persistence.py # Periodic save/load for queues
│ │ │ └── storage.py # In-memory data storage
│ │ └── models/
│ │ └── queue.py # Pydantic models for messages
│ └── main.py # FastAPI app setup
├── mpi_prediction/
│ ├── core/
│ │ └── config.py # Configurations (queue endpoints, model path, etc.)
│ ├── model/
│ │ └── predictor.py # Model loading and prediction helpers
│ ├── queue_client/
│ │ ├── transactions_queue_client.py # Client for pulling transaction requests
│ │ └── results_queue_client.py # Client for pushing prediction results
│ ├── mpi_master.py # MPI master (distributes jobs to workers)
│ ├── mpi_worker.py # MPI worker (runs model predictions)
│ ├── main.py # Entry point (launches master/workers)
│ └── requirements.txt # Dependencies
├── fraud_rf_model.pkl # Pre-trained RandomForest model
├── Dockerfile # Docker build file for each service
├── docker-compose.yml # Compose setup for queue_service and mpi_prediction
└── README.md # This file

---

## How It Works

- Start both services using Docker Compose.
- `queue_service` provides endpoints to push transactions and receive results via HTTP.
- `mpi_prediction` pulls transactions in batches, distributes them across MPI worker processes, and sends predictions back to the results queue.

---

## Usage

1. **Build and start services:**
    ```
    docker compose build
    docker compose up
    ```

2. **Add a transaction request to the queue:**
    ```
    curl -X POST "http://localhost:7500/api/v1/queues/transactions/push" \\
         -H "Content-Type: application/json" \\
         -d '{"transaction_id": "test-001", "data": {"status": "submitted", "vendor_id": 73, "amount": 229.88, "timestamp": 1700000000}}'
    ```

3. **List available queues:**
    ```
    curl http://localhost:7500/api/v1/queues
    ```

4. **Pull the prediction result:**
    ```
    curl http://localhost:7500/api/v1/queues/results/pull
    ```

---

## Main Files Description

### queue_service

- `main.py` - FastAPI app entrypoint.
- `api/v1/queues.py` - Endpoints for creating, pushing, pulling, deleting, and listing queues.
- `core/config.py` - Settings and environment configs.
- `core/logger.py` - Request/response logging.
- `core/persistence.py` - Loads and periodically saves all queues to disk.
- `core/storage.py` - In-memory storage abstraction.
- `models/queue.py` - Pydantic schemas for queue messages.

### mpi_prediction

- `main.py` - Launches MPI master or worker.
- `mpi_master.py` - Master node logic for fetching, distributing, and collecting results.
- `mpi_worker.py` - Worker node logic for running predictions.
- `model/predictor.py` - Loads model, preprocesses requests, performs prediction.
- `queue_client/transactions_queue_client.py` - Gets transactions from the queue.
- `queue_client/results_queue_client.py` - Sends predictions to the results queue.
- `core/config.py` - All runtime config (API base, queue names, model path).

---

## Notes

- Both services auto-create `results` and `transactions` queues on startup.
- The prediction model expects input features to match the training schema (`timestamp`, `status`, `vendor_id`, `amount`).
- Logs and queue states are periodically persisted.
- Batch size and number of workers can be configured via environment variables.

---

## Author

Samir Ibrahimov, IMC Krems, 2025

"""