from discord_connections import Client
from punq import Container

from domain.entities.tokens import Token
from infra.repositories.tokens.base import BaseTokensRepository
from init import init_container
from logic.commands.users import create_user_from_token


async def handle_discord_code(code: str) -> None:
    container: Container = init_container()
    connections_client: Client = container.resolve(Client)
    token = await connections_client.get_token(code)

    tokens_repository: BaseTokensRepository = container.resolve(BaseTokensRepository)
    token = Token(
        access_token=token.access_token,
        refresh_token=token.refresh_token,
        expires_at=token.expires_at
    )
    await tokens_repository.add_token(token)
    await create_user_from_token(token)
