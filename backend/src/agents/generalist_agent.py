import logging

from src.agents.validator_agent import ValidatorAgent
from src.agents.agent import ChatAgentSuccess, ChatAgentFailure
from src.agents import Agent
from src.prompts import PromptEngine
from src.utils import Config

logger = logging.getLogger(__name__)
config = Config()

engine = PromptEngine()


class GeneralistAgent(Agent):
    async def generalist_answer(self, utterance: str) -> ChatAgentSuccess | ChatAgentFailure:
        answer = await self.llm.chat(self.model, engine.load_prompt("generalist-answer", question=utterance), "")
        validator_agent = ValidatorAgent(config.validator_agent_llm, config.validator_agent_model)
        validation = (await validator_agent.validate(f"Task: {utterance}  Answer: {answer}")).lower() == "true"
        if validation:
            return ChatAgentSuccess(self.__class__.__name__, answer)
        else:
            return ChatAgentFailure(self.__class__.__name__, "Generalist Agent did not pass validation.")
