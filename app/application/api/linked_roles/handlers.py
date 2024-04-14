from discord_connections import Client
from fastapi import APIRouter, Depends, status

from fastapi.responses import RedirectResponse
from punq import Container

from application.api.schemas import ErrorSchema
from init import init_container

router = APIRouter(tags=['LinkedRoles'])


@router.get(
    '/',
    status_code=status.HTTP_307_TEMPORARY_REDIRECT,
    description='Redirects to Discord\'s OAuth2 login page.',
    responses=
    {
        status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema}
    }
)
async def linked_roles_handler(
    container: Container = Depends(init_container)
) -> RedirectResponse:
    connections_client: Client = container.resolve(Client)

    url, state = connections_client.oauth_url
    response = RedirectResponse(url)
    response.set_cookie('state', state)

    return response
