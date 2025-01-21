from src.prompts import PromptEngine
from src.agents import Agent
from src.session import get_session_chat
from src.session.file_uploads import get_uploaded_report
import logging
from src.utils.config import Config


config = Config()

engine = PromptEngine()

logger = logging.getLogger(__name__)

report_prompt_template = "The following report was generated from the file {filename}:\n{report_content}"


class IntentAgent(Agent):
    async def determine_intent(self, utterance: str) -> str:
        session_chat = get_session_chat()
        session_report = get_uploaded_report()
        if session_report and session_report.get("filename") and session_report.get("report"):
            report_prompt = report_prompt_template.format(
                filename=session_report.get("filename"),
                report_content=session_report.get("report")
            )
        else:
            report_prompt = "There is no report content"

        return await self.llm.chat(
            self.model,
            engine.load_prompt(
                "intent-system",
                chat_history=session_chat if session_chat else "There is no chat history",
                report_prompt=report_prompt
            ),
            user_prompt=engine.load_prompt(
                "intent",
                question=utterance
            ),
            return_json=True
        )
