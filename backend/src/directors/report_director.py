import sys
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


def prepare_file_for_report(file_contents: bytes, filename: str, file_id:  str):
    file_size = sys.getsizeof(file_contents)

    if file_size > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail=f"File upload must be less than {MAX_FILE_SIZE} bytes")

    session_file = FileUpload(
        id=file_id,
        filename=filename,
        upload_id=None,
        content=None
    )

    update_session_file_uploads(session_file)


async def create_report_from_file(file_contents: bytes, filename: str, file_id:  str) -> ReportResponse:

    file = LLMFile(filename=filename, file=file_contents)

    report_agent = get_report_agent()

    company_name = await report_agent.get_company_name(file)

    topics = await get_materiality_agent().list_material_topics_for_company(company_name)

    report = await report_agent.create_report(file, topics)

    report_response = ReportResponse(
        filename=filename,
        id=file_id,
        report=report,
        answer=create_report_chat_message(filename, company_name, topics),
    )

    store_report(report_response)

    return report_response


def create_report_chat_message(file_name: str, company_name: str, topics: dict[str, str]) -> str:
    topics_with_markdown = [
        f"{key}\n{value}" for key, value in topics.items()
    ]
    topics_summary = "\n\n".join(topics_with_markdown)

    return (
        f"Your report for {file_name} is ready to view.\n\n"
        f"The following materiality topics were identified for {company_name} which the report focuses on:\n\n"
        f"{topics_summary}"
    )
