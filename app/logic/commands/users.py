from discord_connections import Client
from discord_connections.datatypes import Token as DiscordToken
from punq import Container

from domain.entities.tokens import Token
from domain.entities.users import User
from infra.repositories.users.base import BaseUsersRepository
from init import init_container
from logic.exceptions.exceptions import UserWithThatDiscordUserIDAlreadyExistsError


async def create_user_from_token(token: Token) -> None:
    container: Container = init_container()

    connections_client: Client = container.resolve(Client)
    discord_token = DiscordToken(
        access_token=token.access_token,
        refresh_token=token.refresh_token,
        expires_at=token.expires_at
    )
    data = await connections_client.get_user_data(discord_token)

    users_repository: BaseUsersRepository = container.resolve(BaseUsersRepository)
    user = User(
        discord_user_id=int(data['user']['id']),
        discord_token_oid=token.oid
    )

    try:
        await users_repository.add_user(user)
    except UserWithThatDiscordUserIDAlreadyExistsError as e:
        existing_user = e.existing_user
        await users_repository.update_user_by_oid(
            existing_user.oid, {'discord_token_oid': token.oid}
        )
