import logging
from app.core.config import Config

logging.basicConfig(
    filename=Config.LOG_PATH,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - [%(name)s] - %(message)s'
)

def log_message(message: str):
    logging.info(message)
