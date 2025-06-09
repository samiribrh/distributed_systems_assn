from core.config import Config
from model.predictor import load_model, predict

def run_worker(comm, rank):
    """
    Worker process workflow:
    - Loads the ML model
    - Waits for a task from the master
    - Runs prediction
    - Sends result back to master
    """
    print(f"[Worker {rank}] Started", flush=True)
    model = load_model(Config.MODEL_PATH)

    while True:
        print(f"[Worker {rank}] Waiting for task", flush=True)
        request = comm.recv(source=0, tag=11)
        print(f"[Worker {rank}] Got request: {request}", flush=True)
        prediction = predict(model, request)
        print(f"[Worker {rank}] Prediction: {prediction}", flush=True)
        result = {
            "transaction_id": request["transaction_id"],
            "prediction": prediction
        }
        print(f"[Worker {rank}] Sending result: {result}", flush=True)
        comm.send(result, dest=0, tag=22)
