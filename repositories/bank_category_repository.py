import logging
from typing import Any

from psycopg2.extensions import connection

from config.database_connection import get_cursor
from models.bank_category import Category, CategoryCreate

logger = logging.getLogger(__name__)


class BankCategoryRepository:

    def find_by_id(self, id: int, conn: connection | None = None) -> Category | None:
        with get_cursor(conn) as cur:
            cur.execute("SELECT * FROM bankcategory WHERE id = %s", (id,))
            row = cur.fetchone()
        if not row:
            logger.debug("Category ID: id = %d not found", id)
            return None
        return self._to_category(row)

    def find_by_name(
        self, name: str, conn: connection | None = None
    ) -> Category | None:
        with get_cursor(conn) as cur:
            cur.execute("SELECT * FROM bankcategory WHERE name = %s", (name,))
            row = cur.fetchone()
        if not row:
            logger.debug("Category Name: name = %s not found", name)
            return None
        return self._to_category(row)

    def find_all(self, conn: connection | None = None) -> list[Category] | None:
        with get_cursor(conn) as cur:
            cur.execute("SELECT * FROM bankcategory")
            rows = cur.fetchall()
        return [self._to_category(row) for row in rows]

    def exists_by_name(self, name: str, conn: connection | None = None) -> bool:
        with get_cursor(conn) as cur:
            cur.execute("SELECT 1 FROM bankcategory WHERE name = %s", (name,))
            return cur.fetchone() is not None

    def create(
        self, category_data: CategoryCreate, conn: connection | None = None
    ) -> Category:
        with get_cursor(conn) as cur:
            cur.execute(
                "INSERT INTO bankcategory(name, description) VALUES(%s, %s) RETURNING *",
                (category_data.name, category_data.description),
            )
            row = cur.fetchone()
        category = self._to_category(row)
        logger.info(
            "Category created: name = %s, description = %s",
            category.name,
            category.description,
        )
        return category

    def update_by_id(
        self, id: int, category: CategoryCreate, conn: connection | None = None
    ) -> Category | None:
        with get_cursor(conn) as cur:
            cur.execute(
                "UPDATE bankcategory SET name = %s, description = %s WHERE id = %s RETURNING *",
                (category.name, category.description, id),
            )
            row = cur.fetchone()
        if not row:
            logger.debug("Update failed: id = %d does not exist", id)
            return None
        category_updated = self._to_category(row)
        logger.info("Name and Description Updated")
        return category_updated

    def delete_by_id(self, id: int, conn: connection | None = None) -> bool:
        with get_cursor(conn) as cur:
            cur.execute("DELETE FROM bankcategory WHERE id = %s", (id,))
            deleted = cur.rowcount > 0
        logger.info("Category with id = %d deleted", id)
        return deleted

    @staticmethod
    def _to_category(row: dict[str, Any]) -> Category:
        return Category(**row)
