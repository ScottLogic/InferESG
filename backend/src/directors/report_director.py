from fastapi import UploadFile

from src.session.file_uploads import FileUploadReport, store_report
from src.utils.scratchpad import clear_scratchpad, update_scratchpad
from src.utils.file_utils import handle_file_upload
from src.agents import get_report_agent, get_materiality_agent

async def report_on_file_upload(upload: UploadFile) -> FileUploadReport:

    file = handle_file_upload(upload)

    update_scratchpad(result=file["content"])

    topics = await get_materiality_agent().list_material_topics("Astra Zeneca")

    report = await get_report_agent().create_report(file["content"], topics)

    clear_scratchpad()

    report_upload = FileUploadReport(filename=file["filename"], id=file["uploadId"], report=report)

    store_report(report_upload)

    return report_upload
