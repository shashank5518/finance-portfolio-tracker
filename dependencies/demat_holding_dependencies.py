from fastapi import Depends
from sqlalchemy.orm import Session

from config.database_connection import get_db
from repositories.demat_portfolio_repository import DematHoldingRepository


def get_demat_holding_repository(
    db: Session = Depends(get_db),
) -> DematHoldingRepository:
    return DematHoldingRepository(db)
