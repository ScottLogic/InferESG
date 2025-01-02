from typing import Tuple
import logging
from src.utils import get_scratchpad, update_scratchpad
from src.router import get_agent_for_task
from src.agents import get_validator_agent, get_generalist_agent
import json

logger = logging.getLogger(__name__)

no_questions_response = "No questions found to solve"
unsolvable_response = "I am sorry, but I was unable to find an answer to this task"
no_agent_response = "I am sorry, but I was unable to find an agent to solve this task"


async def process_question(question) -> None:
    try:
        (agent_name, answer, status) = await solve_task(question, get_scratchpad())
        update_scratchpad(agent_name, question, answer)
        if status == "error":
            raise Exception(answer)
    except Exception as error:
        update_scratchpad(error=str(error))


async def solve_all(intent_json) -> None:
    questions = intent_json["questions"]

    if len(questions) == 0:
        question = intent_json["question"]
        await process_question(question)
    else:
        for question in questions:
            await process_question(question)


async def solve_task(task, scratchpad, attempt=0) -> Tuple[str, str, str]:
    for attempt in [1, 2, 3, 4]:
        if attempt == 4:
            agent = get_generalist_agent()
        else:
            agent = await get_agent_for_task(task, scratchpad)
        if agent is None:
            raise Exception(no_agent_response)
        logger.info(f"Agent selected: {agent.name}")
        logger.info(f"Task is: {task}")
        answer = await agent.invoke(task)
        parsed_json = json.loads(answer)
        status = parsed_json.get("status", "success")
        ignore_validation = parsed_json.get("ignore_validation", "")
        answer_content = parsed_json.get("content", "")
        if (ignore_validation == "true") or await is_valid_answer(answer_content, task):
            return (agent.name, answer_content, status)
    raise Exception(unsolvable_response)


async def is_valid_answer(answer, task) -> bool:
    is_valid = (await get_validator_agent().invoke(f"Task: {task}  Answer: {answer}")).lower() == "true"
    return is_valid
