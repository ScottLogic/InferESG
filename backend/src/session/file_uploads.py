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
    id: str
    filename: str
    upload_id: Optional[str]


class FileUpload(TypedDict):
    id: str
    filename: str
    upload_id: Optional[str]
    content: Optional[str]


class ReportResponse(TypedDict):
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


def get_session_file_upload(id) -> FileUpload | None:
    return _get_key(UPLOADS_KEY_PREFIX + id)


def update_session_file_uploads(file_upload: FileUpload):
    file_uploads_meta_session = get_session(UPLOADS_META_SESSION_KEY, [])
    if not file_uploads_meta_session:
        # initialise the session object
        set_session(UPLOADS_META_SESSION_KEY, file_uploads_meta_session)

    file_uploads_meta_session.append({"id": file_upload["id"], "filename": file_upload["filename"]})
    redis_client.set(UPLOADS_KEY_PREFIX + file_upload["id"], json.dumps(file_upload))

def get_file_meta_for_filename(filename: str) -> FileUploadMeta | None:
    files = get_session_file_uploads_meta() or []
    for file in files:
        if file["filename"] == filename:
            return file

def get_file_content_for_filename(filename: str) -> str | None:
    file_meta = get_file_meta_for_filename(filename)
    if file_meta:
        file = get_session_file_upload(file_meta["id"])
        return file["content"] if file else None
    return None

def set_file_content_for_filename(filename: str, content:str):
    file_meta = get_file_meta_for_filename(filename)
    if file_meta:
        file = get_session_file_upload(file_meta["id"])
        if file:
            file["content"] = content
            redis_client.set(UPLOADS_KEY_PREFIX + file_meta["id"], json.dumps(file))
        else:
            logger.warning(f"set file content for missing id {id}")
    else:
        logger.warning(f"set file content for missing filename {filename}")

def clear_session_file_uploads():
    logger.info("Clearing file uploads and reports from session")

    meta_list = get_session(UPLOADS_META_SESSION_KEY, [])

    keys = []
    for meta in meta_list:
        keys.append(UPLOADS_KEY_PREFIX + meta["id"])
        keys.append(REPORT_KEY_PREFIX + meta["id"])

    if keys:
        logger.info(f"Deleting keys {keys}")
        for key in keys:
            redis_client.delete(key)

    set_session(UPLOADS_META_SESSION_KEY, [])


def store_report(report: ReportResponse):
    redis_client.set(REPORT_KEY_PREFIX + report["id"], json.dumps(report))


def get_report(id: str) -> ReportResponse | None:
    return _get_key(REPORT_KEY_PREFIX + id)
