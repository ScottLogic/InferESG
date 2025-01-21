import logging
from typing import Tuple, Any

from src.agents.agent import ChatAgentFailure
from src.utils import to_json, Config
from src.prompts import PromptEngine
from src.agents import ChatAgent, get_chat_agents
from src.llm import get_llm

logger = logging.getLogger(__name__)
prompt_engine = PromptEngine()
config = Config()


def find_selected_agent(name: str) -> ChatAgent | None:
    return next((agent for agent in get_chat_agents() if agent.name == name), None)


def create_agent_failure_message(chat_agent_failures: list[ChatAgentFailure]) -> str:
    return f"Take into account the previous agent failure(s): {chat_agent_failures}" if chat_agent_failures else ""


async def select_tool_for_question(
    task: str,
    chat_agent_failures: list[ChatAgentFailure]
) -> Tuple[ChatAgent | None, str, dict[str, Any]]:
    if not config.router_model:
        raise Exception("Router config model missing")

    failed_agents = [failure.agent_name for failure in chat_agent_failures if not failure.retry]

    agents = [
        agent.get_agent_details()
        for agent in get_chat_agents() if agent.name not in failed_agents
    ]
    logger.info("#####  ~  Calling LLM for next best step  ~  #####")
    logger.info(f"Agents: {agents}")
    logger.info(f"Excluded agents: {failed_agents}")

    best_next_step_response = await get_llm(config.router_llm).chat(
        config.router_model,
        prompt_engine.load_prompt("agent-selection-system-prompt"),
        prompt_engine.load_prompt(
            "agent-selection-user-prompt",
            list_of_agents_and_tools=agents,
            agent_failure_message=create_agent_failure_message(chat_agent_failures),
            question=task
        ),
        return_json=True
    )

    best_next_step = to_json(best_next_step_response, "Failed to interpret LLM next step format from step string")
    agent = find_selected_agent(best_next_step["agent"])
    tool_name = best_next_step["tool"]
    parameters = best_next_step["parameters"]

    return agent, tool_name, parameters
