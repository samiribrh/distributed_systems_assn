import time
from core.config import Config
from model.predictor import load_model
from queue_client.transactions_queue_client import fetch_batch_from_queue
from queue_client.results_queue_client import send_result_to_queue

def run_master(comm, size):
    """
    Master process workflow:
    - Continuously fetches up to (size-1) requests from the queue
    - Distributes requests to workers via MPI
    - Collects results from workers
    - Sends results to results queue
    - Sleeps before next fetch
    """

    while True:
        # Fetch up to (size-1) transactions from the queue
        batch = fetch_batch_from_queue(size - 1)
        if not batch:
            # Sleep before next batch
            time.sleep(Config.FETCH_SLEEP_TIME)
            continue  # Block/wait until requests available

        # Distribute each request to a worker
        for i, request in enumerate(batch):
            comm.send(request, dest=i + 1, tag=11)

        # Gather results from each worker
        results = []
        for i in range(len(batch)):
            result = comm.recv(source=i + 1, tag=22)
            results.append(result)

        # Send results to the results queue
        for result in results:
            send_result_to_queue(result)
