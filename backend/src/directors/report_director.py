import sys
import uuid
from fastapi import UploadFile, HTTPException

from src.llm.llm import LLMFile
from src.session.file_uploads import ReportResponse, store_report
from src.agents import get_report_agent, get_materiality_agent

MAX_FILE_SIZE = 10 * 1024 * 1024


async def create_report_from_file(upload: UploadFile) -> ReportResponse:
    file_stream = await upload.read()
    if upload.filename is None or upload.filename == "":
        raise HTTPException(status_code=400, detail="Filename missing from file upload")

    file_size = sys.getsizeof(file_stream)

    if file_size > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail=f"File upload must be less than {MAX_FILE_SIZE} bytes")

    file = LLMFile(file_name=upload.filename, file=file_stream)
    file_id = str(uuid.uuid4())

    report_agent = get_report_agent()

    company_name = await report_agent.get_company_name(file)

    topics = await get_materiality_agent().list_material_topics(company_name)

    report = await report_agent.create_report(file, topics)

    report_response = ReportResponse(
        filename=file.file_name,
        id=file_id,
        report=report,
        answer=create_report_chat_message(file.file_name, company_name, topics),
    )

    store_report(report_response)

    return report_response


def create_report_chat_message(file_name: str, company_name: str, topics: dict[str, str]) -> str:
    topics_with_markdown = [f"{key}\n{value}" for key, value in topics.items()]
    return f"""Your report for {file_name} is ready to view.

The following materiality topics were identified for {company_name} which the report focuses on:

{"\n\n".join(topics_with_markdown)}
"""
