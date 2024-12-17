import logging
from src.prompts import PromptEngine
from src.agents import ChatAgent, chat_agent
from src.utils import Config
from src.utils.web_utils import (
    answer_user_question,
)
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
        try:
            answer_to_user = await answer_user_question(utterance, self.llm, self.model)
            answer_result = json.loads(answer_to_user)
            if answer_result["status"] == "error":
                response = {"content": "Error in finding the answer.", "ignore_validation": "false"}
                return json.dumps(response, indent=4)
            final_answer = json.loads(answer_result["response"]).get("answer", "")
            if not final_answer:
                response = {"content": "Error in answer format.", "ignore_validation": "false"}
                return json.dumps(response, indent=4)
            logger.info(f"Answer found successfully {final_answer}")
            response = {"content": final_answer, "ignore_validation": "false"}
            return json.dumps(response, indent=4)

        except Exception as e:
            logger.error(f"Error in web_general_search_core: {e}")
            return "An error occurred while processing the search query."
