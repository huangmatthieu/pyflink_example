from pyflink_example.models.user import User
from pyflink_example.repository.user_repository import UserRepository
import logging
from typing import Iterable
from typing import TypedDict

logger = logging.getLogger(__name__)


class RawUser(TypedDict):
    id: str
    name: str
    email: str


class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def process(self, raw: RawUser) -> Iterable[User]:
        user = User(
            id=raw["id"],
            name=raw["name"],
            email=raw["email"]
        )

        if "@" not in user.email:
            logger.warning(
                "Invalid email '%s' for user id=%s",
                user.email,
                user.id
            )
            return []

        self.repo.save(user)
        return [user]
