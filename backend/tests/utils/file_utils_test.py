from unittest.mock import MagicMock
from fastapi import HTTPException

import pytest

from src.llm.llm import LLMFile
from src.utils.file_utils import handle_file_upload


def test_handle_file_upload_unsupported_type():
    file_content = b"\x89PNG\r\n\x1a\n\x00\x00\x00IHDR"
    with pytest.raises(HTTPException) as err:
        handle_file_upload(LLMFile(file_name="test.png", file=file_content))

    assert err.value.status_code == 400
    assert err.value.detail == "File upload must be a supported type text or pdf"


def test_handle_file_upload_text(mocker):
    mock = mocker.patch("src.utils.file_utils.update_session_file_uploads", MagicMock())

    file_content = b"Sample text content"
    session_file = handle_file_upload(LLMFile(file_name="test.txt", file=file_content))

    mock.assert_called_with(session_file)


def test_handle_file_upload_pdf(mocker):
    mock = mocker.patch("src.utils.file_utils.update_session_file_uploads", MagicMock())
    pdf_mock = mocker.patch("src.utils.file_utils.PdfReader", MagicMock())
    file_content = b"%PDF-1.4"

    session_file = handle_file_upload(LLMFile(file_name="test.pdf", file=file_content))

    pdf_mock.assert_called_once()
    mock.assert_called_with(session_file)
