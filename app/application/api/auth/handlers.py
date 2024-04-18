from fastapi import APIRouter, status, Depends, HTTPException, BackgroundTasks
from fastapi.requests import Request
from fastapi.responses import RedirectResponse

from application.api.auth.schemas import AuthCallbackSchema
from application.api.schemas import ErrorSchema
from logic.commands.tokens import handle_discord_code

router = APIRouter(tags=['Auth'])


@router.get(
    '/callback',
    description='Callback for Discord OAuth2 authentication.',
    status_code=status.HTTP_307_TEMPORARY_REDIRECT,
    responses={
        status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema},
        status.HTTP_403_FORBIDDEN: {'model': ErrorSchema}
    }
)
async def auth_callback_handler(
    request: Request,
    background_tasks: BackgroundTasks,
    schema: AuthCallbackSchema = Depends(),
) -> RedirectResponse:
    saved_state = request.cookies.get('state')

    if not (saved_state or schema.state) or schema.state != saved_state:
        # TODO log error
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail={'error': 'Invalid status.'})

    background_tasks.add_task(handle_discord_code, code=schema.code)

    return RedirectResponse('https://discord.com/app')
