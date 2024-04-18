from abc import ABC, abstractmethod
from dataclasses import dataclass

from domain.entities.metadata import Metadata


@dataclass
class BaseMetadataRepository(ABC):
    @abstractmethod
    async def save_metadata(self, metadata: Metadata) -> None:
        ...

    @abstractmethod
    async def get_metadata_by_discord_user_id(self, discord_user_id: int) -> Metadata | None:
        ...
