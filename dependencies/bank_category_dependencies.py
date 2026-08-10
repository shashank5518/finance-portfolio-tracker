from fastapi import Depends
from sqlalchemy.orm import Session

from config.database_connection import get_db
from repositories.bank_category_repository import BankCategoryRepository


def get_bank_category_repository(
    db: Session = Depends(get_db),
) -> BankCategoryRepository:
    return BankCategoryRepository(db)
