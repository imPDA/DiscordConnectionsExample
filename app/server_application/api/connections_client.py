from functools import lru_cache

from discord_connections import Client

import environ
env = environ.Env()


@lru_cache(1)
def create_client() -> Client:
    client = Client(
        client_id=env('CLIENT_ID'),
        client_secret=env('CLIENT_SECRET'),
        redirect_uri=env('OAUTH_REDIRECT_URL'),
        discord_token=env('TOKEN')
    )

    return client
