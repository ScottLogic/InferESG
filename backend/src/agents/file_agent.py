import logging

from src.utils.json import to_json
from src.llm.llm import LLMFile
from src.agents.base_chat_agent import BaseChatAgent
from src.prompts.prompting import PromptEngine
from .agent import chat_agent
from .tool import Parameter, ToolActionFailure, ToolActionSuccess, parameterised_tool
from src.utils.config import Config
from src.session.file_uploads import get_file_meta_for_filename, get_session_file_uploads_meta

logger = logging.getLogger(__name__)
config = Config()
engine = PromptEngine()


def generate_files_description(self) -> str:
    file_meta = get_session_file_uploads_meta() or []
    filenames = [file["filename"] for file in file_meta]

    return f"Extract parts of the following files {", ".join(filenames)}"


@parameterised_tool(
    name="read_file",
    description="Extract parts of the content of a text or pdf file",
    parameters={
        "question": Parameter(
            type="string",
            description="The question that is being asked",
        ),
        "filename": Parameter(
            type="string",
            description="The name of the file to extract related information from",
        ),
    },

)
async def read_file(question, filename: str, llm, model)  -> ToolActionSuccess | ToolActionFailure:
    logger.info(f"intent {question} filename {filename}")

    file = get_file_meta_for_filename(filename)
    logger.info(f"file {file}")

    if not file:
        return ToolActionFailure(f"No file {filename} available.")

    final_info = await llm.chat_with_file(
        model,
        system_prompt=engine.load_prompt("extract-text-from-file-system-prompt"),
        user_prompt=question,
        files=[LLMFile(file["filename"], bytes())],
        return_json=True
        )

    return ToolActionSuccess(to_json(final_info))


@chat_agent(
    name="FileAgent",
    description=generate_files_description,
    tools=[read_file]
)
class FileAgent(BaseChatAgent):
    pass
