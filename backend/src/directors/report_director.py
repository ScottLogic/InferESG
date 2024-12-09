
from typing import TypedDict
from fastapi import UploadFile

from src.utils.scratchpad import clear_scratchpad, update_scratchpad
from src.utils.file_utils import handle_file_upload
from src.agents import get_report_agent, get_materiality_agent


class FileUploadReport(TypedDict):
    id: str
    filename: str | None
    report: str | None


async def report_on_file_upload(upload: UploadFile) -> FileUploadReport:

    file = handle_file_upload(upload)

    update_scratchpad(result=file["content"])

    topics = await get_materiality_agent().list_material_topics("Astra Zeneca")

    report = await get_report_agent().create_report(file["content"], topics)

    clear_scratchpad()

    return {"filename": file["filename"], "id": file["uploadId"], "report": report}
