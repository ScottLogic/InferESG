import json
import logging
from typing import Optional

from src.utils import to_json, Config, Scratchpad
from src.prompts import PromptEngine
from src.agents import ChatAgent, get_chat_agents
from src.llm import get_llm

logger = logging.getLogger(__name__)
prompt_engine = PromptEngine()
config = Config()


def find_agent_from_name(name):
    return next((agent for agent in get_chat_agents() if agent.name == name), None)


async def select_agent_for_task(
    task: str,
    scratchpad: Scratchpad,
    excluded_agents: Optional[list[str]] = None
) -> ChatAgent | None:
    if excluded_agents is None:
        excluded_agents = []

    agents = [
        {"name": agent.name, "description": agent.description}
        for agent in get_chat_agents() if agent.name not in excluded_agents
    ]
    logger.info("#####  ~  Calling LLM for next best step  ~  #####")
    logger.info(f"Scratchpad so far: {scratchpad}")

    if not config.router_model:
        raise Exception("Router config model missing")

    best_next_step_response = await get_llm(config.router_llm).chat(
        config.router_model,
        prompt_engine.load_prompt(
            "agent-selection-system-prompt", list_of_agents=json.dumps(agents, indent=4)
        ),
        prompt_engine.load_prompt("agent-selection-user-prompt", task=task),
        return_json=True
    )

    best_next_step = to_json(best_next_step_response, "Failed to interpret LLM next step format from step string")

    return find_agent_from_name(best_next_step["agent_name"])
