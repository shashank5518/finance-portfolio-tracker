import logging
from collections.abc import Sequence

# from psycopg2.extensions import connection
from sqlalchemy import exists, select
from sqlalchemy.orm import Session

from models.bank_category import BankCategory

# from config.database_connection import get_cursor
# from models.bank_category import Category, CategoryCreate

logger = logging.getLogger(__name__)


class BankCategoryRepository:

    def __init__(self, session: Session) -> None:
        self.session = session

    def find_by_id(self, id: int) -> BankCategory | None:
        return self.session.get(BankCategory, id)

    def find_by_name(self, name: str) -> BankCategory | None:
        stmt = select(BankCategory).where(BankCategory.name == name)
        return self.session.execute(stmt).scalar_one_or_none()

    def find_all(self) -> Sequence[BankCategory]:
        stmt = select(BankCategory)
        return self.session.execute(stmt).scalars().all()

    def exists_by_name(self, name: str) -> bool | None:
        stmt = select(exists().where(BankCategory.name == name))
        return self.session.scalar(stmt)

    def create(self, category_data: BankCategory) -> BankCategory:
        self.session.add(category_data)
        self.session.flush()
        logger.info("Category : %s was created", category_data.name)
        return category_data

    def update_by_id(self, id: int, category: BankCategory) -> BankCategory | None:
        category_db = self.session.get(BankCategory, id)
        if category_db is None:
            logger.debug("Category: %d not found", id)
            return None
        category_db.name = category.name
        category_db.description = category.description
        self.session.flush()
        logger.info("Updated category id=%d (name=%s)", id, category.name)
        return category_db

    def delete_by_id(self, id: int) -> bool:
        category = self.session.get(BankCategory, id)
        if category is None:
            logger.debug("Category id: %d was not found", id)
            return False
        self.session.delete(category)
        self.session.flush()
        logger.info("Category id: %d was deleted", id)
        return True
