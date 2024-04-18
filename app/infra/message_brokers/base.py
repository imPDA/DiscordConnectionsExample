from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Dict


@dataclass
class BaseMessageBroker(ABC):
    @abstractmethod
    async def send_message(self, topic: str, value: bytes, key: bytes) -> None:
        ...

    @abstractmethod
    async def consume(self) -> List[Dict]:
        ...
