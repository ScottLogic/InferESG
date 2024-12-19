from abc import ABC

from src.llm import LLMFile


class LLMFileUploadManager(ABC):
    async def upload_files(self, files: list[LLMFile]):
        pass

    async def delete_all_files(self):
        pass
