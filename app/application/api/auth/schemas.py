from pydantic import BaseModel


class AuthCallbackSchema(BaseModel):
    code: str
    state: str
