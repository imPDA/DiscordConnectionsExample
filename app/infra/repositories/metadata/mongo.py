from dataclasses import dataclass

from domain.entities.metadata import Metadata
from infra.repositories.metadata.base import BaseMetadataRepository
from infra.repositories.metadata.converters import (
    convert_metadata_entity_to_document,
    convert_metadata_document_to_entity
)
from infra.repositories.mongo import BaseMongoDBRepository


@dataclass
class MongoDBMetadataRepository(BaseMetadataRepository, BaseMongoDBRepository):
    async def save_metadata(self, metadata: Metadata) -> None:
        await self._collection.find_one_and_replace(
            {'discord_user_id': metadata.discord_user_id},
            convert_metadata_entity_to_document(metadata),
            upsert=True
        )

    async def get_metadata_by_discord_user_id(self, discord_user_id: int) -> Metadata | None:
        metadata_document = await self._collection.find_one(
            filter={'discord_user_id': discord_user_id}
        )

        if not metadata_document:
            return None

        return convert_metadata_document_to_entity(metadata_document)
