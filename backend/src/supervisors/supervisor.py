import asyncio
import logging

from src.agents.agent import ChatAgentSuccess, ChatAgentFailure
from src.utils import update_scratchpad
from src.router import select_tool_for_question
from src.agents import get_generalist_agent

logger = logging.getLogger(__name__)

no_questions_response = "No questions found to solve"
unsolvable_response = "I am sorry, but I was unable to find an answer to this task"
no_agent_response = "I am sorry, but I was unable to find an agent to solve this task"
number_of_attempts = 4


async def solve_questions(questions: list[str]) -> None:
    if len(questions) == 0:
        Exception(no_questions_response)

    tasks = [solve_question(question) for question in questions]

    results = await asyncio.gather(*tasks, return_exceptions=True)

    for i, result in enumerate(results):
        if isinstance(result, ChatAgentSuccess | ChatAgentFailure):
            update_scratchpad(result.agent_name, questions[i], result.answer)
        else:
            update_scratchpad(error=str(result))


async def solve_question(question) -> ChatAgentSuccess:
    chat_agent_failures = []
    for attempt in range(number_of_attempts):
        agent, tool_name, parameters = await select_tool_for_question(question, chat_agent_failures)
        if agent is None:
            break

        answer = await agent.invoke(question, tool_name, parameters)
        logger.info(f"Agent answer: {answer} ")
        if isinstance(answer, ChatAgentSuccess):
            return answer
        else:
            chat_agent_failures.append(answer)

    logger.info("Defaulting to Generalist Agent")
    answer = await get_generalist_agent().generalist_answer(question)
    if isinstance(answer, ChatAgentSuccess):
        return answer
    else:
        raise Exception(f"Could not create answer for question: {question}")
