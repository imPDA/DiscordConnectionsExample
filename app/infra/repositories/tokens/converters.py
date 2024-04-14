from datetime import datetime
from typing import Mapping, Any

from domain.entities.tokens import Token


def convert_token_document_to_entity(token_document: Mapping[str, Any]):
    return Token(
        oid=token_document['oid'],
        access_token=token_document['access_token'],
        refresh_token=token_document['refresh_token'],
        expires_at=datetime.fromisoformat(token_document['expires_at'])
    )


def convert_token_entity_to_document(token: Token):
    return {
        'oid': token.oid,
        'access_token': token.access_token,
        'refresh_token': token.refresh_token,
        'expires_at': token.expires_at.isoformat()
    }
