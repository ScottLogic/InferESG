import json
import logging
from uuid import uuid4

from src.utils.json import try_pretty_print
from src.chat_storage_service import ChatResponse, store_chat_message
from src.utils import clear_scratchpad, update_scratchpad, get_scratchpad
from src.session import update_session_chat
from src.agents import get_intent_agent, get_answer_agent
from src.prompts import PromptEngine
from src.supervisors import solve_all
from src.utils import Config
from src.websockets.connection_manager import connection_manager

logger = logging.getLogger(__name__)
config = Config()
engine = PromptEngine()
director_prompt = engine.load_prompt("director")

async def question(question: str) -> ChatResponse:
    intent = await get_intent_agent().invoke(question)
    intent_json = json.loads(intent)
    update_session_chat(role="user", content=question)
    logger.info(f"Intent determined: {intent}")

    try:
        await solve_all(intent_json)
    except Exception as error:
        logger.error(f"Error during task solving: {error}")
        update_scratchpad(error=str(error))

    current_scratchpad = get_scratchpad()

    for entry in current_scratchpad:
        if entry["agent_name"] == "ChartGeneratorAgent":
            generated_figure = entry["result"]
            await connection_manager.send_chart({"type": "image", "data": generated_figure})
            clear_scratchpad()
            return ChatResponse(id=str(uuid4()),
                                question=question,
                                answer="",
                                reasoning=try_pretty_print(current_scratchpad))

    final_answer = await get_answer_agent().invoke(question)
    update_session_chat(role="system", content=final_answer)
    logger.info(f"final answer: {final_answer}")

    response = ChatResponse(id=str(uuid4()),
                            question=question,
                            answer=final_answer,
                            reasoning=try_pretty_print(current_scratchpad))

    store_chat_message(response)

    clear_scratchpad()

    return response
