import base64
import uuid

token_store = {}

def generate_token(role):
    rand = base64.b64encode(uuid.uuid4().bytes).decode("utf-8")
    return f"{role}:{rand}"
