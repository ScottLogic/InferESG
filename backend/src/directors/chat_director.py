from dataclasses import dataclass
import json
import logging
from typing import Optional
from uuid import uuid4

from src.session.chat_response import update_session_chat_response_ids
from src.utils.json import try_pretty_print
from src.chat_storage_service import ChatResponse, store_chat_message
from src.utils import clear_scratchpad, update_scratchpad, get_scratchpad
from src.session import update_session_chat
from src.agents import get_intent_agent, get_answer_agent
from src.utils.dynamic_knowledge_graph import generate_dynamic_knowledge_graph
from src.prompts import PromptEngine
from src.supervisors.supervisor import solve_questions
from src.utils import Config
from src.utils.graph_db_utils import populate_db, is_db_populated
from src.websockets.connection_manager import connection_manager

logger = logging.getLogger(__name__)
config = Config()
engine = PromptEngine()
director_prompt = engine.load_prompt("chat_director")

@dataclass
class FinalAnswer:
    message: str = ""
    dataset: Optional[str] = None


async def question(question: str) -> ChatResponse:
    intent = await get_intent_agent().determine_intent(question)
    intent_json = json.loads(intent)
    update_session_chat(role="user", content=question)
    logger.info(f"Intent determined: {intent}")

    await solve_questions(intent_json["questions"])

    current_scratchpad = get_scratchpad()

    for entry in current_scratchpad:
        if entry["agent_name"] == "ChartGeneratorAgent":
            generated_figure = entry["result"]
            await connection_manager.send_chart({"type": "image", "data": generated_figure})
            clear_scratchpad()
            return ChatResponse(id=str(uuid4()),
                                question=question,
                                answer="",
                                dataset=None,
                                reasoning=try_pretty_print(current_scratchpad))

    final_answer = FinalAnswer()
    try:
        final_answer = await __create_final_answer(question)
        update_session_chat(role="system", content=final_answer.message)
    except Exception as error:
        logger.error(f"Error during answer generation: {error}", error)
        update_scratchpad(error=str(error))

    logger.info(f"final answer: {final_answer}")

    response = ChatResponse(id=str(uuid4()),
                            question=question,
                            answer=final_answer.message or '',
                            dataset=final_answer.dataset,
                            reasoning=try_pretty_print(current_scratchpad))

    store_chat_message(response)
    update_session_chat_response_ids(response.get("id"))

    clear_scratchpad()

    return response


async def __create_final_answer(question: str) -> FinalAnswer:
    datastore_agents = [scratch for scratch in get_scratchpad() if scratch['agent_name'] == 'DatastoreAgent']
    query_result = datastore_agents[-1]['result'] if datastore_agents else None

    message = await get_answer_agent().create_answer(question)

    return FinalAnswer(message, query_result)


async def dataset_upload() -> None:
    dataset_file = "./datasets/bloomberg.csv"

    if is_db_populated():
        logger.info("Skipping database population as already has data")
        return

    with open(dataset_file, 'r') as file:
        csv_data = [
            [entry for entry in line.strip('\n').split(",")]
            for line in file
        ]

    knowledge_graph_config = await generate_dynamic_knowledge_graph(csv_data)

    populate_db(knowledge_graph_config["cypher_query"], csv_data)
