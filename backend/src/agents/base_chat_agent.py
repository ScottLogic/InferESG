from src.agents import ChatAgent
from src.agents.tool import ToolAnswerType
from src.utils import Config
from src.agents.validator_agent import ValidatorAgent

config = Config()


class BaseChatAgent(ChatAgent):
    async def validate(self, utterance: str, answer: ToolAnswerType) -> bool:
        validator_agent = ValidatorAgent(config.validator_agent_llm, config.validator_agent_model)
        validation = (await validator_agent.validate(f"Task: {utterance}  Answer: {answer}")).lower() == "true"
        return validation
