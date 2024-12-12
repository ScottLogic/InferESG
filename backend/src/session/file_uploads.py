import json
from typing import TypedDict, Optional
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
REPORT_KEY_PREFIX = "report_"


class FileUploadMeta(TypedDict):
    uploadId: str
    filename: str


class FileUpload(TypedDict):
    uploadId: str
    content: str
    filename: str
    contentType: Optional[str]
    size: Optional[int]


class FileUploadReport(TypedDict):
    id: str
    answer: str
    filename: Optional[str]
    report: Optional[str]


def get_session_file_uploads_meta() -> list[FileUploadMeta] | None:
    return get_session(UPLOADS_META_SESSION_KEY, [])


def _get_key(key):
    value = redis_client.get(key)
    if value and isinstance(value, str):
        if parsed_session_data := try_parse_to_json(value):
            return parsed_session_data
    return None


def get_session_file_upload(upload_id) -> FileUpload | None:
    return _get_key(UPLOADS_KEY_PREFIX + upload_id)


def update_session_file_uploads(file_upload: FileUpload):
    file_uploads_meta_session = get_session(UPLOADS_META_SESSION_KEY, [])
    if not file_uploads_meta_session:
        # initialise the session object
        set_session(UPLOADS_META_SESSION_KEY, file_uploads_meta_session)

    file_uploads_meta_session.append({"uploadId": file_upload["uploadId"], "filename": file_upload["filename"]})
    redis_client.set(UPLOADS_KEY_PREFIX + file_upload["uploadId"], json.dumps(file_upload))


def clear_session_file_uploads():
    logger.info("Clearing file uploads and reports from session")

    meta_list = get_session(UPLOADS_META_SESSION_KEY, [])

    keys = []
    for meta in meta_list:
        keys.append(UPLOADS_KEY_PREFIX + meta["uploadId"])
        keys.append(REPORT_KEY_PREFIX + meta["uploadId"])

    if keys:
        keystr = " ".join(keys)
        logger.info("Deleting keys " + keystr)
        redis_client.delete(keystr)

    set_session(UPLOADS_META_SESSION_KEY, [])


def store_report(report: FileUploadReport):
    redis_client.set(REPORT_KEY_PREFIX + report["id"], json.dumps(report))


def get_report(id: str) -> FileUploadReport | None:
    return _get_key(REPORT_KEY_PREFIX + id)
