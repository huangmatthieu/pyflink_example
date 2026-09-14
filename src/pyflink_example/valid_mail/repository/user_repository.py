from typing import Protocol
from pyflink_example.valid_mail.models.user import User


class UserRepository(Protocol):
    def save(self, user: User) -> None:
        pass
