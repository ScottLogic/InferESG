import json
import pytest
from unittest.mock import patch, MagicMock
from uuid import uuid4
from starlette.requests import Request
from starlette.responses import Response
from src.session.redis_session_middleware import (
    get_session,
    reset_session,
    set_session,
    get_redis_session
)

@pytest.fixture
def mock_redis():
    with patch('src.session.redis_session_middleware.redis_client') as mock_redis:
        mock_instance = MagicMock()
        mock_redis.return_value = mock_instance
        yield mock_instance

@pytest.fixture
def mock_request():
    request = MagicMock(spec=Request)
    request.cookies.get.return_value = {}
    request.url.hostname = "redis"
    request.state.session.get.return_value = {}
    return request

@pytest.fixture
def mock_call_next():
    async def call_next(request):
        return Response("test response")
    return call_next

@pytest.fixture
def mock_request_context():
    with patch('src.session.redis_session_middleware.request_context'):
        mock_instance = MagicMock()
        mock_instance.get.return_value.state.session = {}
        yield mock_instance

def test_get_session(mocker, mock_request_context):
    mocker.patch("src.session.redis_session_middleware.request_context", mock_request_context)
    mock_request_context.get.return_value.state.session = {"key": "value"}
    assert get_session("key") == "value"
    assert get_session("nonexistent_key") == []


def test_set_session(mocker, mock_request_context):
    mocker.patch("src.session.redis_session_middleware.request_context", mock_request_context)

    set_session("key", "value")
    assert get_session("key") == "value"


def test_get_redis_session(mocker, mock_request, mock_redis):
    mocker.patch("src.session.redis_session_middleware.redis_client", mock_redis)
    session_id = uuid4()
    mock_request.cookies.get.return_value = session_id
    mock_redis.get.return_value = '{"user_id": 1}'

    mock_redis.set(session_id, json.dumps({"user_id": 1}))
    result = get_redis_session(mock_request)

    assert result == {"user_id": 1}
    mock_redis.get.assert_called_once_with(session_id)

def test_reset_session(mocker, mock_request_context):
    mocker.patch("src.session.redis_session_middleware.request_context", mock_request_context)

    set_session("key1", "value1")
    set_session("key2", "value2")
    assert get_session("key1") == "value1"
    assert get_session("key2") == "value2"

    reset_session()
    assert get_session("key1") == []
    assert get_session("key2") == []
