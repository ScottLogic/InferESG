import json
from typing import Optional
from uuid import uuid4
import redis
from src.utils import test_redis_connection
from src.utils import Config
from src.utils import try_parse_to_json
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
import contextvars
import logging

config = Config()
logger = logging.getLogger(__name__)

REQUEST_CONTEXT_KEY = "redis_session_context"
SESSION_COOKIE_NAME = "session_id"

request_context = contextvars.ContextVar(REQUEST_CONTEXT_KEY)
redis_client = redis.Redis(host=config.redis_host, port=6379, decode_responses=True)


class RedisSessionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_context.set(request)

        redis_healthy = test_redis_connection()

        if (not redis_healthy or ignore_request(request)):
            response = await call_next(request)
        else:
            session_data = get_redis_session(request)
            request.state.session = session_data

            response = await call_next(request)

            session_id = request.cookies.get(SESSION_COOKIE_NAME) or str(uuid4())
            response.set_cookie(
                SESSION_COOKIE_NAME,
                session_id,
                domain=request.url.hostname,
                samesite='strict',
                httponly=True,
                secure=config.redis_host != "redis"
            )

            redis_client.set(session_id, json.dumps(request.state.session))

        return response


def ignore_request(request: Request) -> bool:
    # prevent generating new session for each health check request
    return request.url.path == '/health' or request.method == 'OPTIONS'


def get_session(key: str, default: Optional[list] = None):
    if not default:
        default = []
    request: Request = request_context.get()
    return request.state.session.get(key, default)


def set_session(key: str, value):
    request: Request = request_context.get()
    request.state.session[key] = value


def reset_session():
    logger.info("Reset chat session")
    request: Request = request_context.get()
    request.state.session = {}
    logger.info(f"db size {redis_client.dbsize()}")


def get_redis_session(request: Request):
    session_id = request.cookies.get(SESSION_COOKIE_NAME)
    logger.info(f"Attempting to get session for session_id: {session_id}")
    if session_id:
        session_data = redis_client.get(session_id)
        logger.info(f"***************** Session data retrieved from Redis for {session_id}: {session_data}")
        if session_data and isinstance(session_data, str):
            parsed_session_data = try_parse_to_json(session_data)
            if parsed_session_data:
                return parsed_session_data
    return {}

