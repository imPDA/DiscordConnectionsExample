from functools import lru_cache

from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
from discord_connections import Client as ConnectionsClient, BaseMetadataModel, MetadataField
from discord_connections.datatypes import IntGe, BoolEq, IntLe
from motor.core import AgnosticClient
from motor.motor_asyncio import AsyncIOMotorClient
from punq import Container, Scope

from infra.message_brokers.base import BaseMessageBroker
from infra.repositories.metadata.base import BaseMetadataRepository
from infra.repositories.metadata.mongo import MongoDBMetadataRepository
from infra.repositories.tokens.base import BaseTokensRepository
from infra.repositories.tokens.mongo import MongoDBTokensRepository
from infra.repositories.users.base import BaseUsersRepository
from infra.repositories.users.mongo import MongoDBUsersRepository
from settings.settings import Settings


class MyMetadata(BaseMetadataModel):
    platform_name: str = 'ConnectionsExample'
    age: MetadataField[IntGe] = MetadataField[IntGe](
        key='age',
        name='Age',
        description='or older',
    )
    male: MetadataField[BoolEq] = MetadataField[BoolEq](
        key='male',
        name='Male?',
        description='Is male or not?',
    )
    favourite_number: MetadataField[IntLe] = MetadataField[IntLe](
        key='favourite_number',
        name='Favourite number',
        description='or less',
    )
    like_cats: MetadataField[BoolEq] = MetadataField[BoolEq](
        key='like_cats',
        name='Like cats?',
        description='Yes or not.',
    )


@lru_cache(1)
def init_container() -> Container:
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

    def init_tokens_repository() -> BaseTokensRepository:
        return MongoDBTokensRepository(
            mongo_db_client=client,
            mongo_db_db_name=settings.mongo_db.db_name,
            mongo_db_collection_name=settings.mongo_db.tokens_collection_name,
        )
    container.register(BaseTokensRepository, factory=init_tokens_repository, scope=Scope.singleton)

    def init_users_repository() -> BaseUsersRepository:
        return MongoDBUsersRepository(
            mongo_db_client=client,
            mongo_db_db_name=settings.mongo_db.db_name,
            mongo_db_collection_name=settings.mongo_db.users_collection_name,
        )
    container.register(BaseUsersRepository, factory=init_users_repository, scope=Scope.singleton)

    def init_metadata_repository() -> BaseMetadataRepository:
        return MongoDBMetadataRepository(
            mongo_db_client=client,
            mongo_db_db_name=settings.mongo_db.db_name,
            mongo_db_collection_name=settings.mongo_db.metadata_collection_name,
        )
    container.register(BaseMetadataRepository, factory=init_metadata_repository, scope=Scope.singleton)

    def create_connections_client() -> ConnectionsClient:
        return ConnectionsClient(
            client_id=settings.client_id,
            client_secret=settings.client_secret,
            redirect_uri=settings.oauth_redirect_uri,
            discord_token=settings.discord_token,
            metadata_model=MyMetadata
        )
    container.register(ConnectionsClient, factory=create_connections_client, scope=Scope.singleton)

    def create_message_broker() -> BaseMessageBroker:
        from infra.message_brokers.kafka import KafkaMessageBroker
        broker = KafkaMessageBroker(
            producer=AIOKafkaProducer(bootstrap_servers=settings.kafka.bootstrap_servers),
            consumer=AIOKafkaConsumer(
                settings.kafka.new_metadata_topic,
                bootstrap_servers=settings.kafka.bootstrap_servers,
                group_id=settings.kafka.group_id,
                auto_offset_reset='earliest'
            )
        )

        return broker

    container.register(
        BaseMessageBroker,
        factory=create_message_broker,
        scope=Scope.singleton
    )
    container.resolve(BaseMessageBroker)

    return container
