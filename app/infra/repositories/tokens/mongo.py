from abc import ABC
from dataclasses import dataclass

from motor.core import AgnosticClient

from domain.entities.tokens import Token
from infra.repositories.tokens.base import BaseTokensRepository
from infra.repositories.tokens.converters import (
    convert_token_document_to_entity,
    convert_token_entity_to_document
)


@dataclass
class BaseMongoDBRepository(ABC):
    mongo_db_client: AgnosticClient
    mongo_db_db_name: str
    mongo_db_collection_name: str

    @property
    def _collection(self):
        return self.mongo_db_client[self.mongo_db_db_name][self.mongo_db_collection_name]


@dataclass
class MongoDBTokensRepository(BaseTokensRepository, BaseMongoDBRepository):
    async def add_token(self, token: Token) -> None:
        await self._collection.insert_one(convert_token_entity_to_document(token))

    async def get_token_by_oid(self, oid: str) -> Token | None:
        token_document = await self._collection.find_one(filter={'oid': oid})

        if not token_document:
            return None

        return convert_token_document_to_entity(token_document)
