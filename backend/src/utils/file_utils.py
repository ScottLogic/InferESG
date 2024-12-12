from io import BytesIO, TextIOWrapper
import time
from fastapi import HTTPException
import logging
import uuid

from pypdf import PdfReader
from src.llm.llm import LLMFileFromBytes
from src.session.file_uploads import FileUpload, update_session_file_uploads, get_session_file_upload

logger = logging.getLogger(__name__)

MAX_FILE_SIZE = 10*1024*1024


def handle_file_upload(file: LLMFileFromBytes) -> FileUpload:

    file_size = len(file.file_stream)

    if (file_size or 0) > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail=f"File upload must be less than {MAX_FILE_SIZE} bytes")

    file_stream = BytesIO(file.file_stream)

    all_content = ""
    content_type = "unknown"
    file_name = "uploaded_file_.pdf"

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
            logger.debug(f'Text content {all_content}')

        except Exception as text_error:
            raise HTTPException(
                status_code=400,
                detail="File upload must be a supported type (text/plain or application/pdf)"
            ) from text_error

    session_file = FileUpload(
        uploadId=str(uuid.uuid4()),
        contentType=content_type,
        filename=file_name,
        content=all_content,
        size=file_size,
    )

    update_session_file_uploads(session_file)

    return session_file


def get_file_upload(upload_id) -> FileUpload | None:
    return get_session_file_upload(upload_id)



