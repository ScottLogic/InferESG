import json
import pytest
from unittest.mock import patch, MagicMock
from starlette.requests import Request
from starlette.responses import Response
from src.session.file_uploads import (FileUpload, clear_session_file_uploads_meta, get_session_file_upload,
                                       get_session_file_uploads_meta, update_session_file_uploads)

@pytest.fixture
def mock_redis():
    with patch('src.session.file_uploads.redis_client') as mock_redis:
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

def test_get_session_file_uploads_meta_empty(mocker, mock_request_context):
    mocker.patch("src.session.redis_session_middleware.request_context", mock_request_context)
    assert get_session_file_uploads_meta() == []


def test_set_session(mocker, mock_redis, mock_request_context):
    mocker.patch("src.session.redis_session_middleware.request_context", mock_request_context)
    mocker.patch("src.session.file_uploads.redis_client", mock_redis)
    file = FileUpload(contentType="text/plain", size=4, content="test", uploadId="1234", filename="test.txt")
    file2 = FileUpload(contentType="text/plain", size=5, content="test2", uploadId="12345", filename="test2.txt")

    update_session_file_uploads(file_upload=file)

    assert get_session_file_uploads_meta() == [ {'filename': 'test.txt', 'uploadId': '1234'}]
    mock_redis.set.assert_called_with("file_upload_1234", json.dumps(file))

    update_session_file_uploads(file_upload=file2)
    assert get_session_file_uploads_meta() == [ {'filename': 'test.txt', 'uploadId': '1234'},
                                               {'filename': 'test2.txt', 'uploadId': '12345'}]

    mock_redis.set.assert_called_with("file_upload_12345", json.dumps(file2))


def test_get_session_file_upload(mocker, mock_redis):
    mocker.patch("src.session.file_uploads.redis_client", mock_redis)
    file = FileUpload(contentType="text/plain", size=4, content="test", uploadId="1234", filename="test.txt")
    mock_redis.get.return_value = json.dumps(file)
    assert get_session_file_upload("file_upload_1234") == file


def test_clear_session_file_uploads_meta(mocker, mock_redis, mock_request_context):
    mocker.patch("src.session.file_uploads.redis_client", mock_redis)
    mocker.patch("src.session.redis_session_middleware.request_context", mock_request_context)

    file = FileUpload(contentType="text/plain", size=4, content="test", uploadId="1234", filename="test.txt")
    file2 = FileUpload(contentType="text/plain", size=5, content="test2", uploadId="12345", filename="test2.txt")

    update_session_file_uploads(file_upload=file)

    clear_session_file_uploads_meta()
    assert get_session_file_uploads_meta() == []
    mock_redis.delete.assert_called_with("file_upload_1234")

    update_session_file_uploads(file_upload=file)
    update_session_file_uploads(file_upload=file2)
    assert get_session_file_uploads_meta() == [ {'filename': 'test.txt', 'uploadId': '1234'},
                                               {'filename': 'test2.txt', 'uploadId': '12345'}]

    clear_session_file_uploads_meta()
    assert get_session_file_uploads_meta() == []
    mock_redis.delete.assert_called_with("file_upload_1234 file_upload_12345")

