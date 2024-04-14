from dataclasses import dataclass
from typing import Mapping, Any

from domain.entities.users import User
from infra.repositories.mongo import BaseMongoDBRepository
from infra.repositories.users.base import BaseUsersRepository
from infra.repositories.users.converters import (
    convert_user_entity_to_document, convert_user_document_to_entity
)
from logic.exceptions.exceptions import UserAlreadyExistsError


@dataclass
class MongoDBUsersRepository(BaseUsersRepository, BaseMongoDBRepository):
    async def add_user(self, user: User) -> None:
        existing_user = await self.find_user_by_discord_user_id(user.discord_user_id)
        if existing_user:
            raise UserAlreadyExistsError(existing_user)

        await self._collection.insert_one(convert_user_entity_to_document(user))

    async def update_user_by_oid(self, oid: str, fields: Mapping[str, Any]) -> None:
        await self._collection.update_one(
            {'oid': oid},
            {'$set': fields}
        )

    async def get_user_by_oid(self, oid: str) -> User | None:
        user_document = await self._collection.find_one(filter={'oid': oid})

        if not user_document:
            return None

        return convert_user_document_to_entity(user_document)

    async def find_user_by_discord_user_id(self, discord_user_id: int) -> User | None:
        user_document = await self._collection.find_one(filter={'discord_user_id': discord_user_id})

        if not user_document:
            return None

        return convert_user_document_to_entity(user_document)
