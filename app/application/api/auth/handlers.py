from fastapi import APIRouter, status, Depends
from fastapi.requests import Request
from fastapi.responses import Response, RedirectResponse
from punq import Container

from discord_connections import Client

from domain.entities.tokens import Token
from infra.repositories.tokens.base import BaseTokensRepository
from init import init_container

router = APIRouter(tags=['Auth'])


# TODO: response_model ResponseSchema
@router.get('/callback', status_code=status.HTTP_307_TEMPORARY_REDIRECT)
async def auth_callback_handler(
    request: Request, code: str, state: str,
    container: Container = Depends(init_container)
):
    saved_state = request.cookies.get('state')
    if not (saved_state or state) or state != saved_state:
        # log error
        return Response(status_code=status.HTTP_403_FORBIDDEN)

    connections_client: Client = container.resolve(Client)
    token = await connections_client.get_oauth_token(code)

    tokens_repository: BaseTokensRepository = container.resolve(BaseTokensRepository)
    await tokens_repository.add_token(Token(
        access_token=token.access_token,
        refresh_token=token.refresh_token,
        expires_at=token.expires_at
    ))

    return RedirectResponse('https://discord.com/app')
