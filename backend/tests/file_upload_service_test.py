from io import BytesIO
from typing import BinaryIO
from unittest.mock import MagicMock
from fastapi import HTTPException, UploadFile
from fastapi.datastructures import Headers
import pytest

from src.session.file_uploads import FileUpload
from src.file_upload_service import handle_file_upload

def test_handle_file_upload_size():

    with pytest.raises(HTTPException) as err:
        handle_file_upload(UploadFile(file=BinaryIO(), size=15*1024*1024))

    assert err.value.status_code == 413
    assert err.value.detail == 'File upload must be less than 10485760 bytes'


def test_handle_file_upload_unsupported_type():

    headers = Headers({"content-type": "text/html"})
    with pytest.raises(HTTPException) as err:
        handle_file_upload(UploadFile(file=BinaryIO(), size=15*1024, headers=headers))

    assert err.value.status_code == 400
    assert err.value.detail == 'File upload must be supported type (text/plain or application/pdf)'

def test_handle_file_upload_text(mocker):

    mock = mocker.patch("src.file_upload_service.update_session_file_uploads", MagicMock())

    headers = Headers({"content-type": "text/plain"})
    file = BytesIO(b"test content")
    id = handle_file_upload(UploadFile(file=file, size=12, headers=headers, filename="test.txt"))

    session_file = FileUpload(uploadId=id,
                             contentType="text/plain" ,
                             filename="test.txt",
                             content="test content",
                             size=12)

    mock.assert_called_with(session_file)


def test_handle_file_upload_pdf(mocker):

    mock = mocker.patch("src.file_upload_service.update_session_file_uploads", MagicMock())
    pdf_mock = mocker.patch("src.file_upload_service.PdfReader", MagicMock())


    headers = Headers({"content-type": "application/pdf"})
    id = handle_file_upload(UploadFile(file=BytesIO(), size=12, headers=headers, filename="test.pdf"))

    session_file = FileUpload(uploadId=id,
                             contentType="application/pdf" ,
                             filename="test.pdf",
                             content="",
                             size=12)

    pdf_mock.assert_called_once()
    mock.assert_called_with(session_file)

