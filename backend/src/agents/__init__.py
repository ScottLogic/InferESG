from typing import List

from src.utils import Config
from src.agents.agent import Agent, agent
from src.agents.datastore_agent import DatastoreAgent
from src.agents.web_agent import WebAgent
from src.agents.intent_agent import IntentAgent
from src.agents.tool import tool, Parameter
from src.agents.validator_agent import ValidatorAgent
from src.agents.answer_agent import AnswerAgent
from src.agents.chart_generator_agent import ChartGeneratorAgent
from src.agents.file_agent import FileAgent
from src.agents.report_agent import ReportAgent


config = Config()


def get_validator_agent() -> Agent:
    return ValidatorAgent(config.validator_agent_llm, config.validator_agent_model)


def get_intent_agent() -> Agent:
    return IntentAgent(config.intent_agent_llm, config.intent_agent_model)


def get_answer_agent() -> Agent:
    return AnswerAgent(config.answer_agent_llm, config.answer_agent_model)


def get_report_agent() -> Agent:
    return ReportAgent(config.report_agent_llm, config.report_agent_model)


def agent_details(agent) -> dict:
    return {"name": agent.name, "description": agent.description}


def get_available_agents() -> List[Agent]:
    return [DatastoreAgent(config.datastore_agent_llm, config.datastore_agent_model),
            WebAgent(config.web_agent_llm, config.web_agent_model),
            ChartGeneratorAgent(config.chart_generator_llm,
                                config.chart_generator_model),
            FileAgent(config.file_agent_llm, config.file_agent_model),
            # FS-63 Silencing Math agent - tool is not optimised.
            # MathsAgent(config.maths_agent_llm, config.maths_agent_model),
            ]


def get_agent_details():
    agents = get_available_agents()
    return [agent_details(agent) for agent in agents]


__all__ = [
    "agent",
    "Agent",
    "agent_details",
    "get_agent_details",
    "get_answer_agent",
    "get_intent_agent",
    "get_available_agents",
    "get_validator_agent",
    "get_report_agent",
    "Parameter",
    "tool",
]
