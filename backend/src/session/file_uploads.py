import json
from typing import TypedDict
import logging
import redis

from src.utils.json import try_parse_to_json
from .redis_session_middleware import get_session, set_session
from src.utils import Config

logger = logging.getLogger(__name__)

config = Config()
redis_client = redis.Redis(host=config.redis_host, port=6379, decode_responses=True)

UPLOADS_META_SESSION_KEY = "file_uploads_meta"
UPLOADS_SESSION_KEY = "file_uploads"

UPLOADS_KEY_PREFIX = "file_upload_"


class FileUploadMeta(TypedDict):
    uploadId: str
    filename: str


class FileUpload(TypedDict):
    uploadId: str
    content: str
    filename: str | None
    contentType: str | None
    size: int | None


def get_session_file_uploads_meta() -> list[FileUploadMeta] | None:
    return get_session(UPLOADS_META_SESSION_KEY, [])


def get_session_file_upload(upload_id) -> FileUpload | None:
    value = redis_client.get(UPLOADS_KEY_PREFIX + upload_id)
    if value and isinstance(value, str):
        parsed_session_data = try_parse_to_json(value)
        if parsed_session_data:
            return parsed_session_data
    return None


def update_session_file_uploads(file_upload:FileUpload):
    file_uploads_meta_session = get_session(UPLOADS_META_SESSION_KEY, [])
    if not file_uploads_meta_session:
        # initialise the session object
        set_session(UPLOADS_META_SESSION_KEY, file_uploads_meta_session)

    file_uploads_meta_session.append({"uploadId": file_upload["uploadId"], "filename": file_upload["filename"]})
    redis_client.set(UPLOADS_KEY_PREFIX + file_upload["uploadId"], json.dumps(file_upload))


def clear_session_file_uploads():
    logger.info("Clearing file uploads from session")

    meta_list = get_session(UPLOADS_META_SESSION_KEY, [])

    keys = [ UPLOADS_KEY_PREFIX + meta["uploadId"] for meta in meta_list ]

    keystr = " ".join(keys)
    logger.info("Deleting keys " + keystr)
    redis_client.delete(keystr)

    set_session(UPLOADS_META_SESSION_KEY, [])

