from typing import Mapping, Any

from domain.entities.metadata import Metadata


def convert_metadata_entity_to_document(metadata: Metadata) -> Mapping[str, Any]:
    return {
        'discord_user_id': metadata.discord_user_id,
        'age': metadata.age,
        'sex': metadata.sex,
        'favourite_number': metadata.favourite_number,
        'favourite_animal': metadata.favourite_animal,
    }


def convert_metadata_document_to_entity(metadata_document: Mapping[str, Any]) -> Metadata:
    return Metadata(
        discord_user_id=metadata_document['discord_user_id'],
        age=metadata_document['age'],
        sex=metadata_document['sex'],
        favourite_number=metadata_document['favourite_number'],
        favourite_animal=metadata_document['favourite_animal'],
    )
