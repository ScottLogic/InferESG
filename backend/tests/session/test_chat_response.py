import pytest
from unittest.mock import patch, MagicMock
from src.session.chat_response import (clear_session_chat_response_ids,
                                       get_session_chat_response_ids,
                                       update_session_chat_response_ids)

@pytest.fixture
def mock_request_context():
    with patch('src.session.redis_session_middleware.request_context'):
        mock_instance = MagicMock()
        mock_instance.get.return_value.state.session = {}
        yield mock_instance


def test_session_chat(mocker, mock_request_context):
    mocker.patch("src.session.redis_session_middleware.request_context", mock_request_context)

    update_session_chat_response_ids("one")
    update_session_chat_response_ids("two")
    assert get_session_chat_response_ids() == ["one", "two"]


def test_clear_session_chat(mocker, mock_request_context):
    mocker.patch("src.session.redis_session_middleware.request_context", mock_request_context)

    update_session_chat_response_ids("123")
    assert get_session_chat_response_ids() == ["123"]
    clear_session_chat_response_ids()
    assert get_session_chat_response_ids() == []
