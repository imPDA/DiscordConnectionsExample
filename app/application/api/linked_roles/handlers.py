from discord_connections import Client
from fastapi import APIRouter, Depends
from fastapi.requests import Request
from fastapi.responses import RedirectResponse
from punq import Container

from init import init_container

router = APIRouter(tags=['LinkedRoles'])


@router.get('/')
async def linked_roles_handler(
    request: Request,
    container: Container = Depends(init_container)
):
    connections_client: Client = container.resolve(Client)

    url, state = connections_client.oauth_url
    response = RedirectResponse(url)
    response.set_cookie('state', state)

    return response
