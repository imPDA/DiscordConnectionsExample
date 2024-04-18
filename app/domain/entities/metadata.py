from dataclasses import dataclass, field

from domain.entities.base import BaseEntity


@dataclass(eq=False)
class Metadata(BaseEntity):
    discord_user_id: int = field(kw_only=True)
    age: int = field(kw_only=True)
    sex: str = field(kw_only=True)
    favourite_number: int = field(kw_only=True)
    favourite_animal: str = field(kw_only=True)
