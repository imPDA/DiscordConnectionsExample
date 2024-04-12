from fastapi import APIRouter, status
from fastapi.requests import Request
from fastapi.responses import Response, RedirectResponse

router = APIRouter(tags=['Auth'])


# TODO: response_model ResponseSchema
@router.get('/callback')
async def auth_callback_handler(request: Request, code: str, state: str):
    saved_state = request.cookies.get('state')
    if not (saved_state or state) or state != saved_state:
        # log error
        return Response(status_code=status.HTTP_403_FORBIDDEN)

    # TODO get token and so on

    return RedirectResponse('https://discord.com/app')
