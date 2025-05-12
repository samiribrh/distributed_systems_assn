from pydantic import BaseModel
from typing import List

class Message(BaseModel):
    transaction_id: str
    data: dict

class Queue(BaseModel):
    name: str
    messages: List[Message] = []
