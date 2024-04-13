from abc import ABC

from dataclasses import dataclass, field

from typing import Self
from uuid import uuid4


@dataclass
class BaseEntity(ABC):
    oid: str = field(default_factory=lambda: str(uuid4()))

    def __hash__(self) -> int:
        return hash(self.oid)

    def __eq__(self, __value: Self) -> bool:
        return self.oid == __value.oid
