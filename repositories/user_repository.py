import logging
from collections.abc import Sequence

from sqlalchemy import exists, select
from sqlalchemy.orm import Session

# from psycopg2.extensions import connection
# from config.database_connection import get_cursor
from models.user import User

logger = logging.getLogger(__name__)


class UserRepository:

    def __init__(self, session: Session) -> None:
        self.session = session

    def find_by_id(self, user_id: int) -> User | None:
        return self.session.get(User, user_id)

    def find_by_email(self, email: str) -> User | None:
        stmt = select(User).where(User.email == email)
        return self.session.execute(stmt).scalar_one_or_none()

    def find_all(self) -> Sequence[User]:
        stmt = select(User)
        return self.session.execute(stmt).scalars().all()

    def exists_by_email(self, email: str) -> bool | None:
        stmt = select(exists().where(User.email == email))
        return self.session.scalar(stmt)

    def create(self, new_user: User) -> User:
        self.session.add(new_user)
        self.session.flush()
        logger.info("User created: id = %d, email = %s", new_user.id, new_user.email)
        return new_user

    def update_name(self, user_id: int, name: str) -> User | None:
        user = self.session.get(User, user_id)
        if user is None:
            logger.debug(f"User with {user_id} not found")
            return None

        user.name = name
        self.session.flush()

        logger.info("Updated user %d name to %s", user.id, user.name)
        return user

    def delete(self, user_id: int) -> bool:
        user = self.session.get(User, user_id)

        if user is None:
            logger.debug(f"Deletion of {user_id} failed")
            return False
        self.session.delete(user)
        self.session.flush()
        logger.info(f"Deleted user: {user_id}")

        return True

    # @staticmethod
    # def _to_user(row: dict[str, Any]) -> User:
    #     return User(**row)
