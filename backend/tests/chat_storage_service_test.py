import json
from unittest.mock import MagicMock, patch

import pytest

from src.chat_storage_service import ChatResponse, get_chat_message, store_chat_message

@pytest.fixture
def mock_redis():
    with patch('src.chat_storage_service.redis_client') as mock_redis:
        mock_instance = MagicMock()
        mock_redis.return_value = mock_instance
        yield mock_instance

def test_store_chat_message(mocker, mock_redis):
    mocker.patch('src.chat_storage_service.redis_client', mock_redis)

    message = ChatResponse(id="1", question="Question", answer="Answer", reasoning="Reasoning", dataset="dataset")
    store_chat_message(message)

    mock_redis.set.assert_called_once_with("chat_1", json.dumps(message))


def test_get_chat_message(mocker, mock_redis):
    mocker.patch('src.chat_storage_service.redis_client', mock_redis)

    message = ChatResponse(id="1", question="Question", answer="Answer", reasoning="Reasoning", dataset="dataset")
    mock_redis.get.return_value = json.dumps(message)

    value = get_chat_message("1")

    assert value == message
