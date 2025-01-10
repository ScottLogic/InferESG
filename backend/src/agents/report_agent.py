import asyncio
import json
import logging
from typing import Coroutine

from src.llm.llm import LLMFile
from src.agents import Agent
from src.prompts import PromptEngine
from src.agents.report_questions import QUESTIONS

logger = logging.getLogger(__name__)
engine = PromptEngine()


class ReportAgent(Agent):
    async def create_report(self, file: LLMFile, materiality_topics: dict[str, str]) -> str:
        materiality = materiality_topics if materiality_topics else "No Materiality topics identified."

        async with asyncio.TaskGroup() as tg:
            basic = tg.create_task(self.report_basic_question(file))

            system_prompt = engine.load_prompt("report-question-system-prompt")
            categorized_tasks = {
                category: [
                    {
                        "report_question": question["report_question"],
                        "task": tg.create_task(self.report_category_question(question["prompt"], system_prompt, file)),
                    }
                    for question in QUESTIONS[category]
                ]
                for category in QUESTIONS.keys()
            }

            materiality = tg.create_task(self.report_materiality_question(materiality, file))

        esg_report_result = ""

        for category, tasks in categorized_tasks.items():
            esg_report_result += f"\n## {category}\n"
            for i, task in enumerate(tasks, start=1):
                esg_report_result += f"\n### {i}. {task['report_question']}\n{task['task'].result()}\n"

        report = engine.load_template(
            template_name="report-template",
            basic=basic.result(),
            esg_report_result=esg_report_result,
            materiality=materiality.result()
        )

        report_conclusion = await self.llm.chat(
            self.model,
            system_prompt=engine.load_prompt("create-report-conclusion"),
            user_prompt=f"The document is as follows\n{report}"
        )

        return f"{report}\n\n{report_conclusion}"

    async def get_company_name(self, file: LLMFile) -> str:
        response = await self.llm.chat_with_file(
            self.model,
            system_prompt=engine.load_prompt("find-company-name-from-file-system-prompt"),
            user_prompt=engine.load_prompt("find-company-name-from-file-user-prompt"),
            files=[file],
        )
        return json.loads(response)["company_name"]

    def report_basic_question(self, file: LLMFile) -> Coroutine:
        return self.llm.chat_with_file(
            self.model,
            system_prompt=engine.load_prompt("create-report-basic"),
            user_prompt="Generate an ESG report about the attached document.",
            files=[file],
        )

    def report_category_question(self, question: str, system_prompt: str, file: LLMFile) -> Coroutine:
        return self.llm.chat_with_file(
            self.model,
            system_prompt=system_prompt,
            user_prompt=question,
            files=[file],
        )

    def report_materiality_question(self, materiality: str, file: LLMFile) -> Coroutine:
        return self.llm.chat_with_file(
            self.model,
            system_prompt=engine.load_prompt("create-report-materiality"),
            user_prompt=engine.load_prompt("create-report-materiality-user-prompt", materiality=materiality),
            files=[file],
        )
