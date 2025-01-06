import logging

from src.agents import ChatAgent
from src.utils import Config
from src.prompts import PromptEngine
from src.agents.validator_agent import ValidatorAgent

logger = logging.getLogger(__name__)
engine = PromptEngine()
config = Config()


class BaseChatAgent(ChatAgent):
    async def validate(self, utterance: str, answer: str) -> bool:
        # TODO think whether we need a validator agent, or just validator llm config
        validator_agent = ValidatorAgent(config.validator_agent_llm, config.validator_agent_model)
        validation = (await validator_agent.validate(f"Task: {utterance}  Answer: {answer}")).lower() == "true"
        return validation
