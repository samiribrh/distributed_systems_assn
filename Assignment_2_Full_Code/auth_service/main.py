from fastapi import FastAPI, HTTPException, Request
from auth import authenticate_user, verify_token
from tokens import token_store
from pydantic import BaseModel
import logger

app = FastAPI()
log = logger.get_logger("auth_service")

class LoginRequest(BaseModel):
    username: str
    password: str

@app.post("/auth/login")
def login(request: LoginRequest):
    token = authenticate_user(request.username, request.password)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    log.info(f"Login request for user: {request.username} => Token issued")
    return {"token": token}

@app.get("/auth/verify")
def verify(token: str):
    valid = verify_token(token)
    log.info(f"Token verification for: {token} => {valid}")
    return {"valid": valid}
