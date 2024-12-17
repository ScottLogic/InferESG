from unittest.mock import MagicMock
from fastapi import HTTPException

import pytest

from src.llm.llm import LLMFile
from src.utils.file_utils import extract_text


def test_handle_file_upload_unsupported_type():
    file_content = b"\x89PNG\r\n\x1a\n\x00\x00\x00IHDR"
    with pytest.raises(HTTPException) as err:
        extract_text(LLMFile(filename="test.png", file=file_content))

    assert err.value.status_code == 400
    assert err.value.detail == "File upload must be a supported type text or pdf"


def test_handle_file_upload_pdf(mocker):
    pdf_mock = mocker.patch("src.utils.file_utils.PdfReader", MagicMock())
    file_content = b"%PDF-1.4"

    extract_text(LLMFile(filename="test.pdf", file=file_content))

    pdf_mock.assert_called_once()
