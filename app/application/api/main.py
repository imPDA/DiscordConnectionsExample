import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI

from application.api.auth.handlers import router as auth_router
from application.api.linked_roles.handlers import router as linked_roles_router
from infra.message_brokers.base import BaseMessageBroker
from infra.message_brokers.kafka import KafkaMessageBroker
from init import init_container


@asynccontextmanager
async def lifespan(app: FastAPI):
    container = init_container()
    message_broker: KafkaMessageBroker = container.resolve(BaseMessageBroker)

    # start producer and consumer on startup
    await message_broker.producer.start()
    await message_broker.consumer.start()

    # run consumer in different task. Ideally - move to a separate container
    asyncio.create_task(message_broker.consume())

    yield

    # stop producer and consumer b4 exiting
    await message_broker.producer.stop()
    await message_broker.consumer.stop()


def create_app() -> FastAPI:
    app = FastAPI(
        title='Test Discord connection app',
        description='Simple containerized app for Discord connections on FastAPI',
        docs_url="/api/docs",
        lifespan=lifespan
    )

    app.include_router(auth_router, prefix='/auth')
    app.include_router(linked_roles_router, prefix='/linked-roles')

    return app
