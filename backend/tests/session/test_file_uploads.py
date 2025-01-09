import json
import pytest
from unittest.mock import patch, MagicMock
from starlette.requests import Request
from starlette.responses import Response
from src.session.file_uploads import (
    FileUpload,
    ReportResponse,
    clear_session_file_uploads,
    get_report,
    get_session_file_upload,
    get_session_file_uploads_meta,
    store_report,
    update_session_file_uploads,
)


@pytest.fixture
def mock_redis():
    with patch("src.session.file_uploads.redis_client") as mock_redis:
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
    with patch("src.session.redis_session_middleware.request_context"):
        mock_instance = MagicMock()
        mock_instance.get.return_value.state.session = {}
        yield mock_instance


def test_get_session_file_uploads_meta_empty(mocker, mock_request_context):
    mocker.patch("src.session.redis_session_middleware.request_context", mock_request_context)
    assert get_session_file_uploads_meta() == []


def test_set_session(mocker, mock_redis, mock_request_context):
    mocker.patch("src.session.redis_session_middleware.request_context", mock_request_context)
    mocker.patch("src.session.file_uploads.redis_client", mock_redis)
    file = FileUpload(content="test", id="1234", filename="test.txt", upload_id=None)
    file2 = FileUpload(content="test2", id="12345", filename="test2.txt", upload_id=None)

    update_session_file_uploads(file_upload=file)

    assert get_session_file_uploads_meta() == [{"filename": "test.txt", "id": "1234"}]
    mock_redis.set.assert_called_with("file_upload_1234", json.dumps(file))

    update_session_file_uploads(file_upload=file2)
    assert get_session_file_uploads_meta() == [
        {"filename": "test.txt", "id": "1234"},
        {"filename": "test2.txt", "id": "12345"},
    ]

    mock_redis.set.assert_called_with("file_upload_12345", json.dumps(file2))


def test_get_session_file_upload(mocker, mock_redis):
    mocker.patch("src.session.file_uploads.redis_client", mock_redis)
    file = FileUpload(content="test", id="1234", filename="test.txt", upload_id=None)
    mock_redis.get.return_value = json.dumps(file)
    assert get_session_file_upload("file_upload_1234") == file


def test_clear_session_file_uploads_meta(mocker, mock_redis, mock_request_context):
    mocker.patch("src.session.file_uploads.redis_client", mock_redis)
    mocker.patch("src.session.redis_session_middleware.request_context", mock_request_context)

    file = FileUpload(content="test", id="1234", filename="test.txt", upload_id=None)
    file2 = FileUpload(content="test2", id="12345", filename="test2.txt", upload_id=None)

    update_session_file_uploads(file_upload=file)

    clear_session_file_uploads()
    assert get_session_file_uploads_meta() == []
    mock_redis.delete.assert_any_call("file_upload_1234")
    mock_redis.delete.assert_any_call("report_1234")

    update_session_file_uploads(file_upload=file)
    update_session_file_uploads(file_upload=file2)
    assert get_session_file_uploads_meta() == [
        {"filename": "test.txt", "id": "1234"},
        {"filename": "test2.txt", "id": "12345"},
    ]

    clear_session_file_uploads()
    assert get_session_file_uploads_meta() == []
    mock_redis.delete.assert_any_call("file_upload_1234")
    mock_redis.delete.assert_any_call("report_1234")
    mock_redis.delete.assert_any_call("file_upload_12345")
    mock_redis.delete.assert_any_call("report_12345")

def test_store_report(mocker, mock_redis):
    mocker.patch("src.session.file_uploads.redis_client", mock_redis)
    report = ReportResponse(filename="test.txt", id="12", report="test report", answer="chat message")

    store_report(report)

    mock_redis.set.assert_called_with("report_12", json.dumps(report))


def test_get_report(mocker, mock_redis):
    mocker.patch("src.session.file_uploads.redis_client", mock_redis)

    report = ReportResponse(filename="test.txt", id="12", report="test report", answer="chat message")
    mock_redis.get.return_value = json.dumps(report)

    value = get_report("12")

    assert value == report
    mock_redis.get.assert_called_with("report_12")
