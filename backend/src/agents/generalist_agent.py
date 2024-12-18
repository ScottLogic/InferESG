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
        try:
            answer_to_user = await answer_user_question(utterance, self.llm, self.model)
            answer_result = json.loads(answer_to_user)
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


async def answer_user_question(search_query, llm, model) -> str:
    try:
        summariser_prompt = engine.load_prompt("generalist-answer", question=search_query)
        response = await llm.chat(model, summariser_prompt, "")
        return json.dumps(
            {
                "status": "success",
                "response": response,
                "error": None,
            }
        )
    except Exception as e:
        logger.error(f"Error during create search term: {e}")
        return json.dumps(
            {
                "status": "error",
                "response": None,
                "error": str(e),
            }
        )
