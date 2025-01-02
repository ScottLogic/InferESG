from abc import ABC, ABCMeta, abstractmethod
from os import PathLike
from typing import Any, Coroutine
from .count_calls import count_calls
from dataclasses import dataclass


count_calls_of_functions = ["chat", "chat_with_file"]


@dataclass
class LLMFile(ABC):
    filename: str
    file: PathLike[str] | bytes


class LLMMeta(ABCMeta):
    def __init__(cls, name, bases, namespace):
        super().__init__(name, bases, namespace)
        if not hasattr(cls, "instances"):
            cls.instances = {}

        cls.instances[name.lower()] = cls()

    def __new__(cls, name, bases, attrs):
        for function in count_calls_of_functions:
            if function in attrs:
                attrs[function] = count_calls(attrs[function])

        return super().__new__(cls, name, bases, attrs)


class LLM(ABC, metaclass=LLMMeta):
    @classmethod
    def get_instances(cls):
        return cls.instances

    @abstractmethod
    def chat(
        self,
        model: str,
        system_prompt: str,
        user_prompt: str,
        return_json: bool = False
    ) -> Coroutine[Any, Any, str]:
        pass

    @abstractmethod
    def chat_with_file(
        self,
        model: str,
        system_prompt: str,
        user_prompt: str,
        files: list[LLMFile]
    ) -> Coroutine:
        pass


class LLMFileUploadManager(ABC):
    @abstractmethod
    async def upload_files(self, files: list[LLMFile]) -> list[str]:
        pass

    @abstractmethod
    async def delete_all_files(self):
        pass
