from io import TextIOWrapper
import time
from fastapi import HTTPException, UploadFile
import logging
import uuid

from pypdf import PdfReader
from src.session.file_uploads import FileUpload, update_session_file_uploads, get_session_file_upload

logger = logging.getLogger(__name__)

MAX_FILE_SIZE = 10*1024*1024

def handle_file_upload(file:UploadFile) -> FileUpload:

    if (file.size or 0) > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail=f"File upload must be less than {MAX_FILE_SIZE} bytes")


    all_content = ""
    if ("application/pdf" == file.content_type):

        start_time = time.time()
        pdf_file = PdfReader(file.file)
        all_content = ""
        for page_num in range(len(pdf_file.pages)):
            page_text = pdf_file.pages[page_num].extract_text()
            all_content += page_text
            all_content += "\n"

        end_time = time.time()

        logger.debug(f'PDF content {all_content}')
        logger.info(f"PDF content extracted successfully in {(end_time - start_time)}")


    elif ("text/plain" == file.content_type):
        all_content = TextIOWrapper(file.file, encoding='utf-8').read()
        logger.debug(f'Text content {all_content}')
    else:
        raise HTTPException(status_code=400,
                            detail="File upload must be supported type (text/plain or application/pdf)")

    session_file = FileUpload(uploadId=str(uuid.uuid4()),
                             contentType=file.content_type,
                             filename=file.filename,
                             content=all_content,
                             size=file.size)

    update_session_file_uploads(session_file)

    return session_file

def get_file_upload(upload_id) -> FileUpload | None:
    return get_session_file_upload(upload_id)



