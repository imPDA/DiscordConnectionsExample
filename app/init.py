from functools import lru_cache
from punq import Container, Scope

from motor.motor_asyncio import AsyncIOMotorClient
from motor.core import AgnosticClient

from infra.repositories.tokens.base import BaseTokensRepository
from infra.repositories.tokens.mongo import MongoDBTokensRepository

from discord_connections import Client as ConnectionsClient

from settings.settings import Settings


@lru_cache(1)
def init_container():
    return _init_container()


def _init_container() -> Container:
    container = Container()

    container.register(Settings, instance=Settings(), scope=Scope.singleton)
    settings: Settings = container.resolve(Settings)

    def create_mongodb_client() -> AgnosticClient:
        return AsyncIOMotorClient(
            settings.mongo_db.connection_uri,
            serverSelectionTimeoutMS=3000
        )

    container.register(AsyncIOMotorClient, factory=create_mongodb_client, scope=Scope.singleton)
    client = container.resolve(AsyncIOMotorClient)

    def init_tokens_mongodb_repository() -> BaseTokensRepository:
        return MongoDBTokensRepository(
            mongo_db_client=client,
            mongo_db_db_name=settings.mongo_db.db_name,
            mongo_db_collection_name=settings.mongo_db.tokens_collection_name,
        )

    container.register(BaseTokensRepository, factory=init_tokens_mongodb_repository, scope=Scope.singleton)

    def create_connections_client() -> ConnectionsClient:
        return ConnectionsClient(
            client_id=settings.client_id,
            client_secret=settings.client_secret,
            redirect_uri=settings.oauth_redirect_uri,
            discord_token=settings.discord_token
        )

    container.register(ConnectionsClient, factory=create_connections_client, scope=Scope.singleton)

    return container
