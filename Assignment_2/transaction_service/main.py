from fastapi import FastAPI, Depends, HTTPException, Header
from models import Transaction, Result, Base
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from schemas import TransactionCreate, TransactionUpdate, ResultOut
import logger

Base.metadata.create_all(bind=engine)
app = FastAPI()
log = logger.get_logger("transaction_service")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def check_auth(token: str = Header(...)):
    role = token.split(":")[0]
    if role not in ["Administrator", "Agent"]:
        raise HTTPException(status_code=403, detail="Access denied")

@app.post("/transactions/import", dependencies=[Depends(check_auth)])
def import_transaction(data: TransactionCreate, db: Session = Depends(get_db)):
    trans = Transaction(**data.dict())
    db.add(trans)
    db.commit()
    log.info(f"New transaction imported: {data}")
    return {"msg": "Transaction saved"}

@app.put("/transactions/update/{id}", dependencies=[Depends(check_auth)])
def update_transaction(id: int, data: TransactionUpdate, db: Session = Depends(get_db)):
    trans = db.query(Transaction).get(id)
    if not trans:
        raise HTTPException(status_code=404, detail="Transaction not found")
    for k, v in data.dict(exclude_unset=True).items():
        setattr(trans, k, v)
    db.commit()
    log.info(f"Transaction {id} updated")
    return {"msg": "Transaction updated"}

@app.get("/transactions/results/{transaction_id}", response_model=ResultOut, dependencies=[Depends(check_auth)])
def get_result(transaction_id: int, db: Session = Depends(get_db)):
    result = db.query(Result).filter(Result.transaction_id == transaction_id).first()
    if not result:
        raise HTTPException(status_code=404, detail="Result not found")
    log.info(f"Result fetched for transaction {transaction_id}")
    return result
