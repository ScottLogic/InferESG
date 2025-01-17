import asyncio
import json
import logging

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
            overview = tg.create_task(
                self.llm.chat_with_file(
                    self.model,
                    system_prompt=engine.load_prompt("create-report-overview"),
                    user_prompt="Generate an ESG report about the attached document.",
                    files=[file],
                ),
            )

            categorized_tasks = {
                category: [
                    {
                        "report_heading": question["report_heading"],
                        "task": tg.create_task(
                            self.llm.chat_with_file(
                                self.model,
                                system_prompt=engine.load_prompt("report-question-system-prompt"),
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
        for category, tasks in categorized_tasks.items():
            esg_report_result += f"\n## {category}\n"
            for i, task in enumerate(tasks, start=1):
                esg_report_result += f"\n### {i}. {task['report_heading']}\n{task['task'].result()}\n"

        report = engine.load_template(
            template_name="report-template",
            overview=overview.result(),
            esg_report_result=esg_report_result,
            materiality=materiality.result(),
        )

        report_conclusion = await self.llm.chat(
            self.model,
            system_prompt=engine.load_prompt("create-report-conclusion"),
            user_prompt=f"The document is as follows\n{report}",
        )

        return f"{report}\n\n{report_conclusion}"

    async def get_company_name(self, file: LLMFile) -> str:
        response = await self.llm.chat_with_file(
            self.model,
            system_prompt=engine.load_prompt("find-company-name-from-file-system-prompt"),
            user_prompt=engine.load_prompt("find-company-name-from-file-user-prompt"),
            files=[file],
            return_json=True,
        )
        return json.loads(response)["company_name"]
