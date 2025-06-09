import requests
from core.config import Config

def send_result_to_queue(result):
    """
    Push a result (prediction) to the results queue via the queue service API.

    Args:
        result (dict): Should contain at least 'transaction_id' and 'prediction'.
    """
    url = f"{Config.QUEUE_API_BASE}/queues/{Config.RESULTS_QUEUE}/push"
    payload = {
        "transaction_id": result["transaction_id"],
        "data": {"prediction": result["prediction"]}
    }
    print("[results_queue_client] Sending to:", url)
    print("[results_queue_client] Payload:", payload)

    try:
        response = requests.post(url, json=payload)
        print("[results_queue_client] Response:", response.status_code, response.text)
        if response.status_code != 200:
            print(f"[results_queue_client] Failed to send result: {response.status_code} {response.text}")
    except requests.RequestException as e:
        print(f"[results_queue_client] Error sending result to queue: {e}")
