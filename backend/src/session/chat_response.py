import logging

from .redis_session_middleware import get_session, set_session

logger = logging.getLogger(__name__)

CHAT_RESPONSE_SESSION_KEY = "chatresponse"

def get_session_chat_response_ids() -> list[str]:
    return get_session(CHAT_RESPONSE_SESSION_KEY, [])


def update_session_chat_response_ids(id:str):
    ids = get_session_chat_response_ids()
    ids.append(id)
    set_session(CHAT_RESPONSE_SESSION_KEY, ids)


def clear_session_chat_response_ids():
    set_session(CHAT_RESPONSE_SESSION_KEY, [])
