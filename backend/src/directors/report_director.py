import sys
import uuid
from fastapi import HTTPException
from src.llm.llm import LLMFile
from src.session.file_uploads import (
    FileUpload,
    ReportResponse,
    store_report,
    update_session_file_uploads
)
from src.agents import get_report_agent, get_materiality_agent

MAX_FILE_SIZE = 10 * 1024 * 1024


async def create_report_from_file(file_contents: bytes, filename: str | None, file_id:  str ) -> ReportResponse:
    file_size = sys.getsizeof(file_contents)

    if filename is None or filename == "":
        raise HTTPException(status_code=400, detail="Filename missing from file upload")

    if file_size > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail=f"File upload must be less than {MAX_FILE_SIZE} bytes")


    file = LLMFile(filename=filename, file=file_contents)

    session_file = FileUpload(
        id=file_id,
        filename=file.filename,
        upload_id=None,
        content=None
    )

    update_session_file_uploads(session_file)

    report_agent = get_report_agent()

    company_name = await report_agent.get_company_name(file)

    topics = await get_materiality_agent().list_material_topics_for_company(company_name)

    report = await report_agent.create_report(file, topics)

    report_response = ReportResponse(
        filename=filename,
        id=str(uuid.uuid4()),
        report=report,
        answer=create_report_chat_message(filename, company_name, topics),
    )

    store_report(report_response)

    return report_response


def create_report_chat_message(filename: str, company_name: str, topics: dict[str, str]) -> str:
    report_chat_message = f"Your report for {filename} is ready to view."
    if topics:
        topics_with_markdown = [f"{key}\n{value}" for key, value in topics.items()]
        report_chat_message += f"""

The following materiality topics were identified for {company_name}:

{"\n\n".join(topics_with_markdown)}"""
    return report_chat_message
