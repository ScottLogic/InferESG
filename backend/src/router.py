import logging
from typing import Tuple, Any

from src.utils import to_json, Config, Scratchpad
from src.prompts import PromptEngine
from src.agents import ChatAgent, get_chat_agents
from src.llm import get_llm

logger = logging.getLogger(__name__)
prompt_engine = PromptEngine()
config = Config()


def find_selected_agent(name: str) -> ChatAgent | None:
    return next((agent for agent in get_chat_agents() if agent.name == name), None)


async def select_tool_for_question(
    task: str,
    scratchpad: Scratchpad,
    excluded_agents: list[str]
) -> Tuple[ChatAgent | None, str, dict[str, Any]]:
    if not config.router_model:
        raise Exception("Router config model missing")

    agents = [
        agent.get_agent_details()
        for agent in get_chat_agents() if agent.name not in excluded_agents
    ]
    logger.info("#####  ~  Calling LLM for next best step  ~  #####")
    logger.info(f"Excluded agents: {excluded_agents}")
    logger.info(f"Scratchpad so far: {scratchpad}")

    best_next_step_response = await get_llm(config.router_llm).chat(
        config.router_model,
        prompt_engine.load_prompt("agent-selection-system-prompt"),
        prompt_engine.load_prompt("agent-selection-user-prompt", list_of_agents_and_tools=agents, question=task),
        return_json=True
    )

    best_next_step = to_json(best_next_step_response, "Failed to interpret LLM next step format from step string")
    agent = find_selected_agent(best_next_step["agent"])
    tool_name = best_next_step["tool"]
    parameters = best_next_step["parameters"]

    return agent, tool_name, parameters
