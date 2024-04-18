from dataclasses import dataclass

from domain.entities.users import User
from logic.exceptions.base import LogicError


@dataclass
class UserWithThatDiscordUserIDAlreadyExistsError(LogicError):
    existing_user: User

    @property
    def message(self) -> str:
        return f"User with Discord ID {self.existing_user.discord_user_id} already exists."
