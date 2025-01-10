import logging

from src.agents.agent import ChatAgentSuccess
from src.utils import get_scratchpad, update_scratchpad
from src.router import select_agent_for_task
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


async def solve_question(task, scratchpad) -> ChatAgentSuccess:
    agent = await select_agent_for_task(task, scratchpad)
    unsuccessful_agents = []
    for attempt in range(number_of_attempts):
        if agent is None:
            raise Exception(unsolvable_response if unsuccessful_agents else no_agent_response)

        logger.info(f"Agent selected: {agent.name}. Task is: {task}")
        answer = await agent.invoke(task)
        logger.info(f"Agent answer: {answer} ")
        if isinstance(answer, ChatAgentSuccess):
            return answer
        else:
            is_final_attempt = attempt >= number_of_attempts - 2
            if is_final_attempt:
                agent = get_generalist_agent()
            elif not answer.retry:
                unsuccessful_agents.append(answer.agent_name)
                agent = await select_agent_for_task(task, scratchpad, unsuccessful_agents)
    raise Exception(unsolvable_response)
