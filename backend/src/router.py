import json
import logging
from src.llm.llm import LLM
from src.utils import to_json, Config
from src.utils.log_publisher import publish_log_info, LogPrefix
from src.prompts import PromptEngine
from src.agents import ChatAgent, get_available_agents, get_agent_details
from src.llm import get_llm

logger = logging.getLogger(__name__)
prompt_engine = PromptEngine()
config = Config()


async def build_plan(task, llm: LLM, scratchpad, model):
    agents_details = get_agent_details()
    agent_selection_system_prompt = prompt_engine.load_prompt(
        "agent-selection-system-prompt", list_of_agents=json.dumps(agents_details, indent=4)
    )
    agent_selection_user_prompt = prompt_engine.load_prompt(
        "agent-selection-user-prompt",
        task=json.dumps(task, indent=4),
    )

    # Call model to choose agent
    logger.info("#####  ~  Calling LLM for next best step  ~  #####")
    await publish_log_info(LogPrefix.USER, f"Scratchpad so far: {scratchpad}", __name__)
    best_next_step = await llm.chat(model, agent_selection_system_prompt, agent_selection_user_prompt, return_json=True)

    return to_json(best_next_step, "Failed to interpret LLM next step format from step string")


def find_agent_from_name(name):
    agents = get_available_agents()
    return (agent for agent in agents if agent.name == name)


async def get_agent_for_task(task, scratchpad) -> ChatAgent | None:
    llm = get_llm(config.router_llm)
    model = config.router_model
    plan = await build_plan(task, llm, scratchpad, model)
    agent = next(find_agent_from_name(plan["agent_name"]), None)

    return agent
