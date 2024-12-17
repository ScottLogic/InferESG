import json
import logging

from src.prompts.prompting import PromptEngine
from .agent_types import Parameter
from .agent import ChatAgent, chat_agent
from .tool import tool
from src.utils.config import Config
from src.session.file_uploads import get_session_file_uploads_meta, llm_file_for_company_name

logger = logging.getLogger(__name__)
config = Config()
engine = PromptEngine()


def context_aware_description(self):
    file_meta = get_session_file_uploads_meta() or []
    logger.info(f" file maeta {file_meta}")
    names = [file["company_name"] or "" for file in file_meta]
    # delete None from names?
    logger.info(f" names {names}")
    description=f"Extract parts of the uploaded files for the following companies {",".join(names)}",
    logger.info(f" description {description}")
    return description

@tool(
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
async def read_file(question_intent, company_name: str, llm, model) -> str:
    logger.info(f"intent {question_intent} company {company_name}")

    # find the files that match the company names.
    files = llm_file_for_company_name(company_name)

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

    # todo fix json inclusion here
    response = {"content": final_info}
    return json.dumps(response, indent=4)


@chat_agent(
    name="FileAgent",
    description="This agent is responsible for reading from uploaded files.",
    tools=[read_file],
    description_gen = context_aware_description
)
class FileAgent(ChatAgent):
    pass
