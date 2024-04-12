from discord_connections import Client
from fastapi import APIRouter
from fastapi.requests import Request
from fastapi.responses import RedirectResponse

router = APIRouter(tags=['LinkedRoles'])


@router.get('/')
async def linked_roles_handler(request: Request):
    connections_client: Client = request.app.state.connections_client

    url, state = connections_client.oauth_url
    response = RedirectResponse(url)
    response.set_cookie('state', state)

    return response
