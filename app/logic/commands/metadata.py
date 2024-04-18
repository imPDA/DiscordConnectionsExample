from typing import Any, Mapping

from punq import Container

from domain.entities.metadata import Metadata
from infra.message_brokers.base import BaseMessageBroker
from infra.repositories.metadata.base import BaseMetadataRepository
from init import init_container
from settings.settings import Settings


async def handle_new_metadata(metadata: Mapping[str, Any], discord_user_id: int) -> None:
    container: Container = init_container()
    settings: Settings = container.resolve(Settings)

    metadata_repository: BaseMetadataRepository = container.resolve(BaseMetadataRepository)
    metadata = Metadata(
        discord_user_id=discord_user_id,
        age=metadata['age'],
        sex=metadata['sex'],
        favourite_number=metadata['favourite_number'],
        favourite_animal=metadata['favourite_animal']
    )

    await metadata_repository.save_metadata(metadata)

    message_broker: BaseMessageBroker = container.resolve(BaseMessageBroker)
    await message_broker.send_message(
        topic=settings.kafka.update_metadata_topic, value=b'', key=str(discord_user_id).encode()
    )
