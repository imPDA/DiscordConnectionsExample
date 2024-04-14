from dataclasses import dataclass, field
from datetime import datetime

from domain.entities.base import BaseEntity


@dataclass(eq=False)
class User(BaseEntity):
    discord_user_id: int = field(kw_only=True)
    discord_token_oid: str = field(kw_only=True)
