
import json
import logging
from typing import TypedDict
import redis

from src.utils.json import try_parse_to_json
from src.utils import Config

class ChatResponse(TypedDict):
    id: str
    question:str
    answer: str
    reasoning: str | None

logger = logging.getLogger(__name__)

config = Config()

redis_client = redis.Redis(host=config.redis_host, port=6379, decode_responses=True)

CHAT_KEY_PREFIX = "chat_"

def store_chat_message(chat:ChatResponse):
    redis_client.set(CHAT_KEY_PREFIX + chat["id"], json.dumps(chat))


def get_chat_message(id: str) -> ChatResponse | None:
    value = redis_client.get(CHAT_KEY_PREFIX + id)
    if value and isinstance(value, str):
        parsed_session_data = try_parse_to_json(value)
        if parsed_session_data:
            return parsed_session_data
    return None
