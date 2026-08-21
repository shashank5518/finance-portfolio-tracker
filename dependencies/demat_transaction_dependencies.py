from fastapi import Depends
from sqlalchemy.orm import Session

from config.database_connection import get_db
from dependencies.demat_holding_dependencies import get_demat_holding_repository
from repositories.demat_portfolio_repository import DematHoldingRepository
from repositories.demat_transaction_repository import DematTransactionRepository
from service.demat_transaction_service import DematTransactionService


def get_demat_transaction_repository(
    db: Session = Depends(get_db),
) -> DematTransactionRepository:
    return DematTransactionRepository(db)


def get_demat_transaction_service(
    demat_transaction_repo: DematTransactionRepository = Depends(
        get_demat_transaction_repository
    ),
    holding_repo: DematHoldingRepository = Depends(get_demat_holding_repository),
):
    return DematTransactionService(demat_transaction_repo, holding_repo)
