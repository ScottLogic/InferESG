from typing import Optional

from src.llm import LLM, LLMFileFromPath, LLMFileFromBytes


class MockLLM(LLM):
    async def chat(self, model: str, system_prompt: str, user_prompt: str, return_json=False) -> str:
        return "mocked response"

    async def chat_with_file(
        self,
        model: str,
        system_prompt: str,
        user_prompt: str,
        files_by_path: Optional[list[LLMFileFromPath]] = None,
        files_by_stream: Optional[list[LLMFileFromBytes]] = None
    ) -> str:
        return "mocked response"
