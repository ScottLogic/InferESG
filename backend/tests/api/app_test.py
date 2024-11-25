from fastapi.testclient import TestClient
import pytest
from src.chat_storage_service import ChatResponse
from src.api import app, healthy_response, unhealthy_neo4j_response, chat_fail_response

client = TestClient(app)
utterance = "Hello there"
expected_message = "Hello to you too! From InferESG"


def test_health_check_response_healthy(mocker):
    mock_test_connection = mocker.patch("src.api.app.test_connection", return_value=True)

    response = client.get("/health")

    mock_test_connection.assert_called()
    assert response.status_code == 200
    assert response.json() == healthy_response


def test_health_check_response_neo4j_unhealthy(mocker):
    mock_test_connection = mocker.patch("src.api.app.test_connection", return_value=False)

    response = client.get("/health")

    mock_test_connection.assert_called()
    assert response.status_code == 500
    assert response.json() == unhealthy_neo4j_response


def test_chat_response_success(mocker):
    mock_question = mocker.patch("src.api.app.question", return_value=expected_message)

    response = client.get(f"/chat?utterance={utterance}")

    mock_question.assert_called_with(utterance)
    assert response.status_code == 200
    assert response.json() == expected_message


def test_chat_response_failure(mocker):
    mock_question = mocker.patch("src.api.app.question", return_value=expected_message)
    mock_question.side_effect = Exception("An error occurred")

    response = client.get(f"/chat?utterance={utterance}")

    mock_question.assert_called_with(utterance)
    assert response.status_code == 500
    assert response.json() == chat_fail_response

def test_chat_delete(mocker):
    mock_reset_session = mocker.patch("src.api.app.reset_session")
    mock_clear_files = mocker.patch("src.api.app.clear_session_file_uploads")

    response = client.delete("/chat")

    mock_clear_files.assert_called_once()
    mock_reset_session.assert_called_once()

    assert response.status_code == 204

def test_chat_message_success(mocker):
    message = ChatResponse(id="1", question="Question", answer="Answer", reasoning="Reasoning")
    mock_get_chat_message = mocker.patch("src.api.app.get_chat_message", return_value=message)

    response = client.get("/chat/123")

    mock_get_chat_message.assert_called_with("123")
    assert response.status_code == 200
    assert response.json() == message

def test_chat_message_not_found(mocker):
    mock_get_chat_message = mocker.patch("src.api.app.get_chat_message", return_value=None)

    response = client.get("/chat/123")

    mock_get_chat_message.assert_called_with("123")
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_lifespan_populates_db(mocker) -> None:
    mock_dataset_upload = mocker.patch("src.api.app.dataset_upload", return_value=mocker.Mock())

    with client:
        mock_dataset_upload.assert_called_once_with()
