from typing import TypedDict
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
import contextvars
import logging

logger = logging.getLogger(__name__)


class Answer(TypedDict):
    agent_name: str | None
    question: str | None
    result: str | None
    error: str | None

scratchpad_context = contextvars.ContextVar("scratchpad", default=[])

Scratchpad = list[Answer]

class ScratchPadMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        scratchpad_context.set([])
        return await call_next(request)

def get_scratchpad() -> Scratchpad:
    return scratchpad_context.get()


def update_scratchpad(agent_name=None, question=None, result=None, error=None):
    get_scratchpad().append({"agent_name": agent_name, "question": question, "result": result, "error": error})


def clear_scratchpad():
    logger.debug("Scratchpad cleared")
    get_scratchpad().clear()
