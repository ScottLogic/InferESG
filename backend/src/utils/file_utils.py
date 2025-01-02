from io import BytesIO, TextIOWrapper
from pathlib import Path
import sys
import time
from fastapi import HTTPException
import logging
import uuid
from os import PathLike
from pypdf import PdfReader
from src.llm.llm import LLMFile
from src.session.file_uploads import FileUpload, get_session_file_upload, update_session_file_uploads

logger = logging.getLogger(__name__)


def handle_file_upload(file: LLMFile) -> FileUpload:
    if isinstance(file.file, (PathLike, str)):
        file_path = Path(file.file)
        with file_path.open("rb") as f:
            file_bytes = f.read()
    elif isinstance(file.file, bytes):
        file_bytes = file.file
    else:
        raise HTTPException(status_code=400, detail="File must be provided as bytes or a valid file path.")

    file_stream = BytesIO(file_bytes)
    file_size = sys.getsizeof(file_bytes)

    all_content = ""
    content_type = "unknown"

    try:
        pdf_file = PdfReader(file_stream)
        content_type = "application/pdf"

        start_time = time.time()
        for page_num in range(len(pdf_file.pages)):
            page_text = pdf_file.pages[page_num].extract_text()
            all_content += page_text
            all_content += "\n"
        end_time = time.time()

        logger.info(f"PDF content extracted successfully in {(end_time - start_time):.2f} seconds")

    except Exception as pdf_error:
        logger.warning(f"Failed to parse file as PDF: {pdf_error}")
        file_stream.seek(0)

        try:
            content_type = "text/plain"
            all_content = TextIOWrapper(file_stream, encoding="utf-8").read()
            logger.debug(f"Text content extracted: {all_content[:100]}...")

        except Exception as text_error:
            raise HTTPException(
                status_code=400, detail="File upload must be a supported type text or pdf"
            ) from text_error

    session_file = FileUpload(
        uploadId=str(uuid.uuid4()),
        contentType=content_type,
        filename=file.filename,
        content=all_content,
        size=file_size,
    )

    update_session_file_uploads(session_file)

    return session_file


def get_file_upload(upload_id) -> FileUpload | None:
    return get_session_file_upload(upload_id)
