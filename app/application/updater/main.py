import asyncio

from aiokafka import AIOKafkaConsumer, TopicPartition
from discord_connections import Client as ConnectionsClient
from discord_connections.datatypes import Token as DiscordToken
from pydantic import ValidationError

from infra.repositories.metadata.base import BaseMetadataRepository
from infra.repositories.tokens.base import BaseTokensRepository
from infra.repositories.users.base import BaseUsersRepository
from init import init_container
from settings.settings import Settings


async def main():
    container = init_container()
    settings: Settings = container.resolve(Settings)

    consumer = AIOKafkaConsumer(
        settings.kafka.update_metadata_topic,
        bootstrap_servers=settings.kafka.bootstrap_servers,
        group_id='updater-group',
        enable_auto_commit=False,  # NO AUTO COMMIT!
        auto_offset_reset='earliest',
    )

    users_repository: BaseUsersRepository = container.resolve(BaseUsersRepository)
    tokens_repository: BaseTokensRepository = container.resolve(BaseTokensRepository)
    metadata_repository: BaseMetadataRepository = container.resolve(BaseMetadataRepository)
    connections_client: ConnectionsClient = container.resolve(ConnectionsClient)

    await consumer.start()

    try:
        async for msg in consumer:
            discord_user_id = int(msg.key.decode())
            metadata = await metadata_repository.get_metadata_by_discord_user_id(
                discord_user_id=discord_user_id
            )
            if not metadata:
                print(f"Can't find metadata for Discord user ID {discord_user_id}.")
                continue

            user = await users_repository.find_user_by_discord_user_id(
                discord_user_id=discord_user_id
            )
            if not user:
                print(f"Can't find user by Discord user ID {discord_user_id}.")
                continue

            token = await tokens_repository.get_token_by_oid(user.discord_token_oid)
            if not token:
                print(f"Can't find Discord token for user {user.oid}.")
                continue

            discord_token = DiscordToken(
                access_token=token.access_token,
                refresh_token=token.refresh_token,
                expires_at=token.expires_at
            )

            data = await connections_client.get_user_data(discord_token)
            username = data['user']['username']

            try:
                metadata_model = connections_client._metadata_model
                metadata = metadata_model(
                    platform_username=username,
                    age=metadata.age,
                    male=metadata.sex == 'male',
                    favourite_number=metadata.favourite_number,
                    like_cats=metadata.favourite_animal.lower() == 'cat',
                )
            except ValidationError as e:
                print("Metadata isn't valid")
                print(e)
                print(metadata.__dict__)
                continue

            try:
                await connections_client.push_metadata(
                    token=discord_token,
                    metadata=metadata
                )
            except Exception as e:
                print("Failed to update metadata: ", e)
            else:
                response = await connections_client.get_metadata(token=discord_token)
                print(f"Metadata_pushed: {response} for user {discord_user_id}")

                tp = TopicPartition(msg.topic, msg.partition)
                await consumer.commit({tp: msg.offset + 1})
    finally:
        await consumer.stop()


if __name__ == "__main__":
    asyncio.run(main())

# TODO all prints -> logging
