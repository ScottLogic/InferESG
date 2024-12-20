import json
import logging

import redis

from src.utils.json import try_parse_to_json
from src.utils import Config

logger = logging.getLogger(__name__)

config = Config()
redis_client = redis.Redis(host=config.redis_host, port=6379, decode_responses=True)

UPLOAD_SESSION_KEY = "llm_file_upload"


def get_all_files() -> list[dict[str, str]]:
    session = redis_client.get(UPLOAD_SESSION_KEY)
    if session and isinstance(session, str):
        data = try_parse_to_json(session)
        if isinstance(data, list):
            return data
    return []


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
    files.append({"file_id": file_id, "filename": filename})
    redis_client.set(UPLOAD_SESSION_KEY, json.dumps(files))
