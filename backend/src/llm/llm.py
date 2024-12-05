from abc import ABC, ABCMeta, abstractmethod
from typing import Any, Coroutine
from .count_calls import count_calls


count_calls_of_functions = ["chat", "chat_with_file"]


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
    def chat(self, model: str, system_prompt: str, user_prompt: str, return_json=False) -> Coroutine[Any, Any, str]:
        pass


class LLMChatWithFile(ABC, metaclass=LLMMeta):
    @classmethod
    def get_instances(cls):
        return cls.instances

    @abstractmethod
    def chat_with_file(
        self,
        model: str,
        system_prompt: str,
        user_prompt: str,
        file_paths: list[str]
    ) -> Coroutine:
        pass
