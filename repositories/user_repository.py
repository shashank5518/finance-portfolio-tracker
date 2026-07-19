import logging
from typing import Any

from psycopg2.extensions import connection

from config.database_connection import get_cursor
from models.user import User, UserCreate

logger = logging.getLogger(__name__)


class UserRepository:

    def find_by_id(self, user_id: int, conn: connection | None = None) -> User | None:
        with get_cursor(conn) as cur:
            cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))
            row = cur.fetchone()
        if not row:
            logger.debug("User not found: id=%d", user_id)
            return None
        return self._to_user(row)

    def find_by_email(self, email: str, conn: connection | None = None) -> User | None:
        with get_cursor(conn) as cur:
            cur.execute("SELECT * FROM users WHERE email = %s", (email,))
            row = cur.fetchone()
            return self._to_user(row) if row else None

    def find_all(self, conn: connection | None = None) -> list[User]:
        with get_cursor(conn) as cur:
            cur.execute("SELECT * FROM users ORDER BY created_at DESC")
            rows = cur.fetchall()
        return [self._to_user(row) for row in rows]

    def exists_by_email(self, email: str, conn: connection | None = None) -> bool:
        with get_cursor(conn) as cur:
            cur.execute("SELECT 1 FROM users WHERE email = %s", (email,))
            return cur.fetchone() is not None

    def create(self, user_data: UserCreate, conn: connection | None = None) -> User:
        with get_cursor(conn) as cur:
            cur.execute(
                "INSERT INTO users(name, email, password_hash) VALUES (%s, %s, %s) RETURNING *",
                (user_data.name, user_data.email, user_data.password_hash),
            )
            row = cur.fetchone()
        user = self._to_user(row)
        logger.info("User created: id = %d, email = %s", user.id, user.email)
        return user

    def update_name(
        self, user_id: int, new_name: str, conn: connection | None = None
    ) -> User | None:
        with get_cursor(conn) as cur:
            cur.execute(
                "UPDATE users SET name = %s WHERE id = %s RETURNING *",
                (new_name, user_id),
            )
            row = cur.fetchone()
        if not row:
            logger.debug("Update failed - User not found: id = %d", user_id)
            return None
        user = self._to_user(row)
        logger.info("User Updated: id = %d name = %s", user.id, user.name)
        return user

    def delete(self, user_id: int, conn: connection | None = None) -> bool:
        with get_cursor(conn) as cur:
            cur.execute("DELETE FROM users WHERE id = %s", (user_id,))
            deleted = cur.rowcount > 0
        logger.info("User delete: id = %d success = %s", user_id, deleted)
        return deleted

    @staticmethod
    def _to_user(row: dict[str, Any]) -> User:
        return User(**row)
