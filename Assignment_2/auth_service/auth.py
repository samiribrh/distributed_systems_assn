from tokens import generate_token, token_store

users_db = {
    "admin": {"password": "adminpass", "role": "Administrator"},
    "secretary": {"password": "secretarypass", "role": "Secretary"},
    "agent": {"password": "agentpass", "role": "Agent"}
}

def authenticate_user(username, password):
    user = users_db.get(username)
    if user and user["password"] == password:
        token = generate_token(user["role"])
        token_store[token] = user["role"]
        return token
    return None

def verify_token(token):
    return token in token_store
