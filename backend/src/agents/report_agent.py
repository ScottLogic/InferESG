import asyncio
import json
import logging

from src.llm.llm import LLMFile
from src.agents import Agent
from src.prompts import PromptEngine
from src.agents.report_questions import QUESTIONS

logger = logging.getLogger(__name__)
engine = PromptEngine()


question_system_prompt = """
The user will provide a report from a company. Your goal is to analyse the document and respond answering the following question in a consise manner.
Include all points that are relivent to the question, be thorough. For each point include as much detail as possible, focus on statistics and evidence from the report in the points.

Format your answer in markdown
Your answer should not contain any headings, instead use bold text
"""  # noqa: E501


class ReportAgent(Agent):
    async def create_report(self, file: LLMFile, materiality_topics: dict[str, str]) -> str:
        materiality = materiality_topics if materiality_topics else "No Materiality topics identified."

        async with asyncio.TaskGroup() as tg:
            basic = tg.create_task(
                self.llm.chat_with_file(
                    self.model,
                    system_prompt=engine.load_prompt("create-report-basic"),
                    user_prompt="Generate an ESG report about the attached document.",
                    files=[file],
                ),
            )

            categorized_tasks = {
                category: [
                    {
                        "basic_question": question["basic_question"],
                        "task": tg.create_task(
                            self.llm.chat_with_file(
                                self.model,
                                system_prompt=question_system_prompt,
                                user_prompt=question["prompt"],
                                files=[file],
                            ),
                        ),
                    }
                    for question in QUESTIONS[category]
                ]
                for category in QUESTIONS.keys()
            }

            materiality = tg.create_task(
                self.llm.chat_with_file(
                    self.model,
                    system_prompt=engine.load_prompt("create-report-materiality"),
                    user_prompt=engine.load_prompt("create-report-materiality-user-prompt", materiality=materiality),
                    files=[file],
                ),
            )

        esg_report_result = ""
        for category in categorized_tasks.keys():
            question_count = 1
            esg_report_result = (
                esg_report_result
                + f"""
## {category}
"""
            )
            for category_task in categorized_tasks[category]:
                esg_report_result = (
                    esg_report_result
                    + f"""
### {question_count}. {category_task["basic_question"]}
{category_task["task"].result()}
"""
                )
                question_count += 1

        result = f"""
{basic.result()}

{esg_report_result}

# Materiality
{materiality.result()}"""

        report_conclusion = await self.llm.chat(
            self.model,
            system_prompt=engine.load_prompt("create-report-conclusion"),
            user_prompt=f"""The document is as follows
{result}""",
        )

        result = f"""
{result}

{report_conclusion}"""

        return result

    async def get_company_name(self, file: LLMFile) -> str:
        response = await self.llm.chat_with_file(
            self.model,
            system_prompt=engine.load_prompt("find-company-name-from-file-system-prompt"),
            user_prompt=engine.load_prompt("find-company-name-from-file-user-prompt"),
            files=[file],
        )
        return json.loads(response)["company_name"]
