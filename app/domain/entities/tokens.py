from dataclasses import dataclass, field
from datetime import datetime

from domain.entities.base import BaseEntity


@dataclass(eq=False)
class Token(BaseEntity):
    access_token: str = field(kw_only=True)
    refresh_token: str = field(kw_only=True)
    expires_at: datetime = field(kw_only=True)

    @property
    def expired(self) -> bool:
        return self.expires_at < datetime.now()
