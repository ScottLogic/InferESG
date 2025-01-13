from dataclasses import dataclass
from enum import Enum
from typing import Callable, Dict

from fastapi import WebSocket


class MessageTypes(Enum):
    PING = "ping"
    PONG = "pong"
    CHAT = "chat"
    LOG = "log"
    IMAGE = "image"
    CONFIRMATION = "confirmation"
    REPORT_IN_PROGRESS = "report:in-progress"
    REPORT_COMPLETE = "report:complete"
    REPORT_CANCELLED = "report:cancelled"
    REPORT_FAILED = "report:failed"


@dataclass
class Message:
    type: MessageTypes
    data: str | None


Handler = Callable[[WebSocket, Callable, str | None], None]
Handlers = Dict[MessageTypes, Handler]
