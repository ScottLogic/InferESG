import json
import logging
from typing import TypedDict

import redis

from src.utils.json import try_parse_to_json
# from .redis_session_middleware import get_session, set_session
from src.utils import Config

logger = logging.getLogger(__name__)

config = Config()
redis_client = redis.Redis(host=config.redis_host, port=6379, decode_responses=True)

UPLOAD_SESSION_KEY = "llm_file_upload"


def get_all_files() -> list[dict[str, str]]:
    session = redis_client.get(UPLOAD_SESSION_KEY)
    return try_parse_to_json(redis_client.get(UPLOAD_SESSION_KEY)) if session else []


class LLMFileUpload(TypedDict):
    file_id: str
    filename: str


def get_llm_file_upload(filename: str) -> str | None:
    files = get_all_files()
    for file in files:
        if file["filename"] == filename:
            return file["file_id"]
    return None


def add_llm_file_upload(file_id: str, filename: str):
    files = get_all_files()
    if not files:
        files = []
    files.append(LLMFileUpload(file_id=file_id, filename=filename))
    redis_client.set(UPLOAD_SESSION_KEY, json.dumps(files))
