from io import BytesIO
from fastapi import UploadFile
from fastapi.datastructures import Headers
from src.llm import MockLLM
import pytest

from src.session.file_uploads import FileUpload
from src.directors.report_director import report_on_file_upload


@pytest.mark.asyncio
async def test_report_on_file_upload(mocker):

    file_upload = FileUpload(uploadId="1", filename="test.txt", content="test", contentType="text/plain", size=4)

    mock_handle_file_upload = mocker.patch("src.directors.report_director.handle_file_upload", return_value=file_upload)
    mock_llm = mocker.patch("src.agents.get_llm", return_value=MockLLM())

    headers = Headers({"content-type": "text/plain"})
    file = BytesIO(b"test content")
    request_upload_file = UploadFile(file=file, size=12, headers=headers, filename="test.txt")
    response = await report_on_file_upload(request_upload_file)

    mock_handle_file_upload.assert_called_once_with(request_upload_file)
    mock_llm.assert_called_once_with("test content")
    assert response == {"filename": "test.txt", "id": "1", "report": "#Report on upload as markdown"}
