from typing import TypedDict
import logging

from .redis_session_middleware import get_session, set_session

logger = logging.getLogger(__name__)

CHAT_SESSION_KEY = "chat"

class Message(TypedDict):
    role: str | None # user or system
    content: str | None


def get_session_chat() -> list[Message] | None:
    return get_session(CHAT_SESSION_KEY, [])


def update_session_chat(role=None, content=None):
    chat_session = get_session(CHAT_SESSION_KEY, [])
    if not chat_session:
        chat_session = []
    chat_session.append({"role": role, "content": content})
    set_session(CHAT_SESSION_KEY, chat_session)


def clear_session_chat():
    set_session(CHAT_SESSION_KEY, [])
