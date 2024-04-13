from fastapi import FastAPI

from .auth.handlers import router as auth_router
from .linked_roles.handlers import router as linked_roles_router


def create_app() -> FastAPI:
    app = FastAPI(
        title='Test Discord connection app',
        description='Simple containerized app for Discord connections on FastAPI',
        docs_url="/api/docs"
    )

    app.include_router(auth_router, prefix='/auth')
    app.include_router(linked_roles_router, prefix='/linked-roles')

    return app
