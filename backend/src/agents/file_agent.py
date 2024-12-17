import json
import logging

from src.agents.base_chat_agent import BaseChatAgent
from src.prompts.prompting import PromptEngine
from .agent import chat_agent
from .tool import Parameter, ToolActionFailure, ToolActionSuccess, parameterised_tool
from src.utils.config import Config
from src.session.file_uploads import get_session_file_uploads_meta, get_llm_files_for_company_name

logger = logging.getLogger(__name__)
config = Config()
engine = PromptEngine()


def generate_files_description(self) -> str:
    file_meta = get_session_file_uploads_meta() or []
    names = [company for company in [file["company_name"] for file in file_meta] if company is not None]
    description=f"Extract parts of the uploaded files and reports for the following companies {",".join(names)}"

    return description

@parameterised_tool(
    name="read_file",
    description="Extract parts of the content of a text file",
    parameters={
        "question_intent": Parameter(
            type="string",
            description="This represents the overall intent the question is attempting to answer",
        ),
        "company_name": Parameter(
            type="string",
            description="The name of the company this request relates to",
        ),
    },

)
async def read_file(question_intent, company_name: str, llm, model)  -> ToolActionSuccess | ToolActionFailure:
    logger.info(f"intent {question_intent} company {company_name}")

    files = get_llm_files_for_company_name(company_name)

    user_prompt = engine.load_prompt(
        "extract-text-from-file-user-prompt",
        question=question_intent
    )

    final_info = await llm.chat_with_file(
        model,
        system_prompt=engine.load_prompt("extract-text-from-file-system-prompt"),
        user_prompt=user_prompt,
        files=files
        )

    response = {"content": json.loads(final_info)}
    return ToolActionSuccess(response)


@chat_agent(
    name="FileAgent",
    description=generate_files_description,
    tools=[read_file]
)
class FileAgent(BaseChatAgent):
    pass
