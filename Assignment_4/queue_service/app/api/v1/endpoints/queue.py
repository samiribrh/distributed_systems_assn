from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.models.queue import Message
from app.core.config import Config
from app.core.logger import log_message
from app.core.storage import storage

router = APIRouter()

class QueueName(BaseModel):
    queue_name: str

@router.post('/queues')
async def create_queue(queue: QueueName):
    queue_name = queue.queue_name
    if queue_name in storage.get_queues():
        log_message(f"Failed to create queue {queue_name} - Already exists")
        raise HTTPException(status_code=400, detail='Queue already exists')
    storage.get_queues()[queue_name] = {'messages': []}
    log_message(f'Queue {queue_name} created')
    return {'status': 'queue created'}


@router.post('/queues/{queue_name}/push')
async def push_message(queue_name: str, message: Message):
    if queue_name not in storage.get_queues():
        log_message(f"Failed to push to {queue_name} - Queue not found")
        raise HTTPException(status_code=404, detail='Queue not found')
    if len(storage.get_queues()[queue_name]['messages']) >= Config.MAX_QUEUE_SIZE:
        log_message(f"Failed to push to {queue_name} - Queue is full")
        raise HTTPException(status_code=400, detail=f'Queue is full (max size: {Config.MAX_QUEUE_SIZE})')
    storage.get_queues()[queue_name]['messages'].append(message.model_dump())
    log_message(f'Pushed to {queue_name}: {message}')
    return {'status': 'message pushed'}

@router.get('/queues/{queue_name}/pull')
async def pull_message(queue_name: str):
    if queue_name not in storage.get_queues() or not storage.get_queues()[queue_name]['messages']:
        log_message(f"Failed to pull from queue {queue_name} - Queue empty or does not exist")
        raise HTTPException(status_code=404, detail='Queue is empty or does not exist')
    message = storage.get_queues()[queue_name]['messages'].pop(0)
    log_message(f'Pulled from {queue_name}: {message}')
    return message

@router.delete('/queues/{queue_name}')
async def delete_queue(queue_name: str):
    if queue_name not in storage.get_queues():
        raise HTTPException(status_code=404, detail='Queue not found')
    del storage.get_queues()[queue_name]
    log_message(f'Queue {queue_name} deleted')
    return {'status': 'queue deleted'}

@router.get('/queues')
async def list_queues():
    return list(storage.get_queues().keys())
