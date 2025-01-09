from src.agents import ChatAgent
from src.utils import Config
from src.agents.validator_agent import ValidatorAgent

config = Config()


class BaseChatAgent(ChatAgent):
    async def validate(self, utterance: str, answer: str) -> bool:
        validator_agent = ValidatorAgent(config.validator_agent_llm, config.validator_agent_model)
        validation = (await validator_agent.validate(f"Task: {utterance}  Answer: {answer}")).lower() == "true"
        return validation
