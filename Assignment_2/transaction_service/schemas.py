from pydantic import BaseModel
from typing import Optional
import datetime

class TransactionCreate(BaseModel):
    customer: str
    status: str
    vendor_id: str
    amount: float

class TransactionUpdate(BaseModel):
    customer: Optional[str]
    status: Optional[str]
    vendor_id: Optional[str]
    amount: Optional[float]

class ResultOut(BaseModel):
    id: int
    transaction_id: int
    timestamp: datetime.datetime
    is_fraudulent: bool
    confidence: float
