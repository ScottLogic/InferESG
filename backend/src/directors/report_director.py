
from typing import TypedDict
from fastapi import UploadFile

from src.utils.scratchpad import clear_scratchpad, update_scratchpad
from src.utils.file_utils import handle_file_upload
from src.agents import get_report_agent


class FileUploadReport(TypedDict):
    id: str
    filename: str | None
    report: str | None


async def report_on_file_upload(upload: UploadFile) -> FileUploadReport:

    file = handle_file_upload(upload)

    update_scratchpad(result=file["content"])

    report = await get_report_agent().invoke(file["content"])

    clear_scratchpad()

    return {"filename": file["filename"], "id": file["uploadId"], "report": report}
