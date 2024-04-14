from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import TypeVar, Generic

MP = TypeVar('MP')
MC = TypeVar('MC')


@dataclass
class BaseMessageBroker(ABC, Generic[MP, MC]):
    producer: MP = field(init=False)
    consumer: MC = field(init=False)

    @abstractmethod
    async def send_message(self, topic: str, value: bytes) -> None:
        ...

    async def consume(self) -> bytes:
        ...
