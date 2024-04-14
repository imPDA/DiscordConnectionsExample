import asyncio
from dataclasses import dataclass
from typing import List

from aiokafka import AIOKafkaProducer, AIOKafkaConsumer, ConsumerRecord

from infra.message_brokers.base import BaseMessageBroker


@dataclass
class KafkaMessageBroker(BaseMessageBroker[AIOKafkaProducer, AIOKafkaConsumer]):
    bootstrap_server: str

    def __post__init__(self):
        self.producer = AIOKafkaProducer(bootstrap_servers=self.bootstrap_server)
        self.consumer = AIOKafkaConsumer('test', bootstrap_servers=self.bootstrap_server)

    # TODO: how and then to start the broker?
    # async def start(self) -> None:
    #     await self.producer.start()
    #     await self.consumer.start()

    async def send_message(self, topic: str, value: bytes) -> None:
        await self.producer.start()  # TODO: refactor later
        await self.producer.send_and_wait(topic=topic, value=value)

    async def consume(self) -> List[ConsumerRecord]:
        await self.consumer.start()  # TODO: refactor later

        records = []

        async for msg in self.consumer:
            print(f"{msg.topic}:{msg.partition:d}:{msg.offset:d}: {msg.key=} {msg.value=} {msg.timestamp=}")
            records.append(msg)

        return records

    async def stop(self) -> None:
        await self.producer.stop()
        await self.consumer.stop()

    def __del__(self) -> None:
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                loop.create_task(self.stop())
            else:
                loop.run_until_complete(self.stop())
        except Exception:
            pass
