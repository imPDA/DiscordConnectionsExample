from typing import Mapping, Any

from domain.entities.users import User


def convert_user_document_to_entity(user_document: Mapping[str, Any]):
    return User(
        oid=user_document['oid'],
        discord_user_id=user_document['discord_user_id'],
        discord_token_oid=user_document['discord_token_oid']
    )


def convert_user_entity_to_document(user: User):
    return {
        'oid': user.oid,
        'discord_user_id': user.discord_user_id,
        'discord_token_oid': user.discord_token_oid
    }
