from abc import ABC, ABCMeta, abstractmethod
from os import PathLike
from typing import Any, Coroutine, Optional
from .count_calls import count_calls
from dataclasses import dataclass


count_calls_of_functions = ["chat", "chat_with_file"]


@dataclass
class LLMFileBase(ABC):
    file_name: str


@dataclass
class LLMFileFromPath(LLMFileBase):
    file_path: PathLike[str]


@dataclass
class LLMFileFromBytes(LLMFileBase):
    file_stream: bytes


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
        files_by_path: Optional[list[LLMFileFromPath]] = None,
        files_by_stream: Optional[list[LLMFileFromBytes]] = None,
        return_json: bool = False
    ) -> Coroutine:
        pass
