import logging

from src.llm import LLM
from src.prompts import PromptEngine
from src.agents import chat_agent
from src.agents.base_chat_agent import BaseChatAgent
from src.agents.tool import utterance_tool, ToolActionSuccess, ToolActionFailure
from src.utils import Config

logger = logging.getLogger(__name__)
config = Config()

engine = PromptEngine()


@utterance_tool(
    name="find_information_content",
    description="Finds the information from the content."
)
async def generalist_answer(utterance: str, llm: LLM, model: str) -> ToolActionSuccess | ToolActionFailure:
    response = await llm.chat(model, engine.load_prompt("generalist-answer", question=utterance), "")
    return ToolActionSuccess(response)


@chat_agent(
    name="GeneralistAgent",
    description="This agent attempts to answer a general question using only the llm",
    tools=[generalist_answer],
)
class GeneralistAgent(BaseChatAgent):
    pass
