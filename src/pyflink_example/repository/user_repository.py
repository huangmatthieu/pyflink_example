from typing import Protocol
from pyflink_example.models.user import User


class UserRepository(Protocol):
    def save(self, user: User) -> None:
        pass
