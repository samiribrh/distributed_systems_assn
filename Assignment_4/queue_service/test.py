import requests
import json

BASE_URL = "http://localhost:7500/api/v1/queues"
HEADERS = {"Content-Type": "application/json"}

def create_queue(queue_name):
    data = {"queue_name": queue_name}
    response = requests.post(BASE_URL, data=json.dumps(data), headers=HEADERS)
    print("Create Queue:", response.status_code, response.json())

def list_queues():
    response = requests.get(BASE_URL)
    print("List Queues:", response.status_code, response.json())

def push_message(queue_name, transaction_id, data):
    url = f"{BASE_URL}/{queue_name}/push"
    message = {"transaction_id": transaction_id, "data": data}
    response = requests.post(url, data=json.dumps(message), headers=HEADERS)
    print("Push Message:", response.status_code, response.json())

def pull_message(queue_name):
    url = f"{BASE_URL}/{queue_name}/pull"
    response = requests.get(url)
    print("Pull Message:", response.status_code, response.json())

def delete_queue(queue_name):
    url = f"{BASE_URL}/{queue_name}"
    response = requests.delete(url)
    print("Delete Queue:", response.status_code, response.json())

def non_existent_pull():
    url = f"{BASE_URL}/nonexistent_queue/pull"
    response = requests.get(url)
    print("Pull from Non-Existent Queue:", response.status_code, response.json())

def overflow_queue():
    create_queue("overflow_test")
    for i in range(12):  # Assuming max size is 10
        push_message("overflow_test", str(i), {"key": f"value_{i}"})

print("1. Creating Queue")
create_queue("test_queue")

print("\n2. Listing Queues")
list_queues()

print("\n3. Pushing Message")
push_message("test_queue", "12345", {"key": "value"})

print("\n4. Pulling Message")
pull_message("test_queue")

print("\n5. Pulling from Empty Queue")
pull_message("test_queue")

print("\n6. Handling Non-Existent Queue")
non_existent_pull()

print("\n7. Overflow Queue Test")
overflow_queue()

print("\n8. Deleting Queue")
delete_queue("test_queue")

print("\n9. Verifying Deletion")
list_queues()
