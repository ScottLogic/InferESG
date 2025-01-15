import logging

from src.agents.agent import ChatAgentSuccess
from src.utils import get_scratchpad, update_scratchpad
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

    for question in questions:
        try:
            result = await solve_question(question, get_scratchpad())
            update_scratchpad(result.agent_name, question, result.answer)
        except Exception as error:
            update_scratchpad(error=str(error))


async def solve_question(question, scratchpad) -> ChatAgentSuccess:
    unsuccessful_agents = []
    for attempt in range(number_of_attempts):
        agent, tool_name, parameters = await select_tool_for_question(question, scratchpad, unsuccessful_agents)
        if agent is None:
            break

        answer = await agent.invoke(question, tool_name, parameters)
        logger.info(f"Agent answer: {answer} ")
        if isinstance(answer, ChatAgentSuccess):
            return answer
        else:
            if not answer.retry:
                unsuccessful_agents.append(answer.agent_name)

    logger.info("Defaulting to Generalist Agent")
    return await get_generalist_agent().generalist_answer(question)
