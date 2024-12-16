import logging
import uuid
from fastapi import UploadFile

from src.llm.llm import LLMFile
from src.session.file_uploads import FileUploadReport, store_report
from src.agents import get_report_agent, get_materiality_agent

logger = logging.getLogger(__name__)

async def report_on_file_upload(upload: UploadFile) -> FileUploadReport:

    file_stream = await upload.read()
    if upload.filename is None:
        raise ValueError("Filename cannot be None")
    file = LLMFile(file_name=upload.filename, file=file_stream)
    file_id = str(uuid.uuid4())

    report_agent = get_report_agent()

    company_name = await report_agent.get_company_name(file)
    logger.info(f"Company name: {company_name}")

    topics = await get_materiality_agent().list_material_topics(company_name)

    logger.info(f"Topics are: {topics}")
    report = await report_agent.create_report(file, topics)
    logger.info(f"Report: {report}")

    report_upload = FileUploadReport(
        filename=file.file_name,
        id=file_id,
        report=report,
        answer=create_report_chat_message(file.file_name, company_name, topics)
    )

    store_report(report_upload)

    return report_upload


def create_report_chat_message(file_name: str, company_name: str, topics: dict[str, str]) -> str:
    topics_with_markdown = [
        f"{key}\n{value}" for key, value in topics.items()
    ]
    return f"""Your report for {file_name} is ready to view.

The following materiality topics were identified for {company_name} which the report focuses on:

{"\n\n".join(topics_with_markdown)}
"""
