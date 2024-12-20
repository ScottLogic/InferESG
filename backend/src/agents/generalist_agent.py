import logging
from src.prompts import PromptEngine
from src.agents import ChatAgent, chat_agent
from src.utils import Config
import json

logger = logging.getLogger(__name__)
config = Config()

engine = PromptEngine()


@chat_agent(
    name="GeneralistAgent",
    description="This agent attempts to answer a general question using only the llm",
    tools=[],
)
class GeneralistAgent(ChatAgent):
    async def invoke(self, utterance) -> str:
        summariser_prompt = engine.load_prompt("generalist-answer", question=utterance)
        response = await self.llm.chat(self.model, summariser_prompt, "")
        return json.dumps({"content": response, "ignore_validation": "false"}, indent=4)
