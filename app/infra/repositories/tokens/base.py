from abc import ABC, abstractmethod
from dataclasses import dataclass

from domain.entities.tokens import Token


@dataclass
class BaseTokensRepository(ABC):
    @abstractmethod
    async def add_token(self, token: Token) -> None:
        ...

    @abstractmethod
    async def get_token_by_oid(self, oid: str) -> Token:
        ...
