from typing import List

from src.utils import Config
from src.agents.agent import Agent, ChatAgent, chat_agent
from src.agents.datastore_agent import DatastoreAgent
from src.agents.web_agent import WebAgent
from src.agents.intent_agent import IntentAgent
from src.agents.tool import tool, Parameter
from src.agents.validator_agent import ValidatorAgent
from src.agents.answer_agent import AnswerAgent
from src.agents.chart_generator_agent import ChartGeneratorAgent
from src.agents.report_agent import ReportAgent
from src.agents.materiality_agent import MaterialityAgent
from src.agents.generalist_agent import GeneralistAgent


config = Config()


def get_validator_agent() -> ChatAgent:
    return ValidatorAgent(config.validator_agent_llm, config.validator_agent_model)


def get_intent_agent() -> ChatAgent:
    return IntentAgent(config.intent_agent_llm, config.intent_agent_model)


def get_answer_agent() -> ChatAgent:
    return AnswerAgent(config.answer_agent_llm, config.answer_agent_model)


def get_report_agent() -> ReportAgent:
    return ReportAgent(config.report_agent_llm, config.report_agent_model)


def get_materiality_agent() -> MaterialityAgent:
    return MaterialityAgent(config.materiality_agent_llm, config.materiality_agent_model)


def get_generalist_agent() -> GeneralistAgent:
    return GeneralistAgent(config.intent_agent_llm, config.intent_agent_model)


def agent_details(agent: ChatAgent) -> dict:
    return {"name": agent.name, "description": agent.description}


def get_available_agents() -> List[ChatAgent]:
    return [
        DatastoreAgent(config.datastore_agent_llm, config.datastore_agent_model),
        WebAgent(config.web_agent_llm, config.web_agent_model),
        ChartGeneratorAgent(config.chart_generator_llm, config.chart_generator_model),
    ]


def get_agent_details():
    agents = get_available_agents()
    return [agent_details(agent) for agent in agents]


__all__ = [
    "Agent",
    "ChatAgent",
    "chat_agent",
    "agent_details",
    "get_agent_details",
    "get_answer_agent",
    "get_intent_agent",
    "get_available_agents",
    "get_validator_agent",
    "get_report_agent",
    "get_materiality_agent",
    "Parameter",
    "tool",
]
