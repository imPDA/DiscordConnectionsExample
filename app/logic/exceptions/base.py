from dataclasses import dataclass

from domain.exceptions.base import ApplicationError


@dataclass(eq=False)
class LogicError(ApplicationError):
    @property
    def message(self) -> str:
        return "Logic error occurred"
