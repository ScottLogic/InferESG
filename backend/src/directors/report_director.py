from fastapi import UploadFile

from src.session.file_uploads import FileUploadReport, store_report
from src.utils.file_utils import handle_file_upload
from src.agents import get_report_agent, get_materiality_agent


async def report_on_file_upload(upload: UploadFile) -> FileUploadReport:

    file = handle_file_upload(upload)

    report_agent = get_report_agent()

    company_name = await report_agent.get_company_name(file["content"])

    topics = await get_materiality_agent().list_material_topics(company_name)

    report = await get_report_agent().create_report(file["content"], topics)

    report_upload = FileUploadReport(
        filename=file["filename"],
        id=file["uploadId"],
        report=report,
        answer=create_report_chat_message(file["filename"], company_name, topics)
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
