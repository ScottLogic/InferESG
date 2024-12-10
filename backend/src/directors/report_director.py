from typing import TypedDict
from src.llm.llm import LLMFileFromBytes
from fastapi import UploadFile

from src.utils.scratchpad import clear_scratchpad, update_scratchpad
from src.agents import get_report_agent
from src.prompts import PromptEngine

engine = PromptEngine()


class FileUploadReport(TypedDict):
    filename: str | None
    report: str | None


async def report_on_file_upload(upload: UploadFile) -> FileUploadReport:
    file_stream = await upload.read()
    if upload.filename is None:
        raise ValueError("Filename cannot be None")

    file = LLMFileFromBytes(file_name=upload.filename, file_stream=file_stream)

    report = await get_report_agent().create_report(file)

    clear_scratchpad()

    return {"filename": file.file_name, "report": report}
