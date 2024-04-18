import json
from dataclasses import dataclass

from aiokafka import AIOKafkaProducer, AIOKafkaConsumer

from infra.message_brokers.base import BaseMessageBroker
from logic.commands.metadata import handle_new_metadata


@dataclass
class KafkaMessageBroker(BaseMessageBroker):
    producer: AIOKafkaProducer
    consumer: AIOKafkaConsumer

    async def send_message(self, topic: str, key: bytes, value: bytes) -> None:
        await self.producer.send_and_wait(topic=topic, value=value, key=key)

    async def consume(self) -> None:
        async for msg in self.consumer:
            print(f"{msg.topic}:{msg.partition}:{msg.offset}: key={msg.key}"
                  f" value={msg.value} timestamp_ms={msg.timestamp}")
            try:
                await handle_new_metadata(
                    metadata=json.loads(msg.value.decode()),
                    discord_user_id=int(msg.key.decode())
                )
            except Exception as e:
                print(f"Error occurred during message consuming: {e}")
