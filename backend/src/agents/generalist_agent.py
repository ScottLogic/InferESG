import logging

from src.agents.agent import ChatAgentSuccess
from src.agents import Agent
from src.prompts import PromptEngine
from src.utils import Config

logger = logging.getLogger(__name__)
config = Config()

engine = PromptEngine()


class GeneralistAgent(Agent):
    async def generalist_answer(self, utterance: str) -> ChatAgentSuccess:
        answer = await self.llm.chat(self.model, engine.load_prompt("generalist-answer", question=utterance), "")
        return ChatAgentSuccess(self.__class__.__name__, answer)
