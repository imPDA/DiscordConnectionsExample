from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Mapping, Any

from domain.entities.users import User


@dataclass
class BaseUsersRepository(ABC):
    @abstractmethod
    async def add_user(self, user: User) -> None:
        ...

    @abstractmethod
    async def get_user_by_oid(self, oid: str) -> User | None:
        ...

    @abstractmethod
    async def update_user_by_oid(self, oid: str, fields: Mapping[str, Any]) -> None:
        ...

    @abstractmethod
    async def find_user_by_discord_user_id(self, discord_user_id: int) -> User | None:
        ...
