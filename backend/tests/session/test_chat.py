import pytest
from unittest.mock import patch, MagicMock
from src.session import get_session_chat, update_session_chat, clear_session_chat

@pytest.fixture
def mock_request_context():
    with patch('src.session.redis_session_middleware.request_context'):
        mock_instance = MagicMock()
        mock_instance.get.return_value.state.session = {}
        yield mock_instance


def test_session_chat(mocker, mock_request_context):
    mocker.patch("src.session.redis_session_middleware.request_context", mock_request_context)

    update_session_chat(role="user", content="Hello")
    update_session_chat(role="system", content="Hi there")
    assert get_session_chat() == [
        {"role": "user", "content": "Hello"},
        {"role": "system", "content": "Hi there"}
    ]


def test_clear_session_chat(mocker, mock_request_context):
    mocker.patch("src.session.redis_session_middleware.request_context", mock_request_context)

    update_session_chat(role="user", content="Hello")
    assert get_session_chat() == [{"role": "user", "content": "Hello"}]
    clear_session_chat()
    assert get_session_chat() == []
