from fastapi import Depends
from sqlalchemy.orm import Session

from config.database_connection import get_db
from dependencies.bank_account_dependencies import get_bank_account_repository
from dependencies.bank_category_dependencies import get_bank_category_repository
from repositories.bank_account_repository import BankAccountRepository
from repositories.bank_category_repository import BankCategoryRepository
from repositories.bank_transaction_repository import BankTransactionRepository
from service.bank_transaction_service import BankTransactionService


def get_bank_transaction_repository(db: Session = Depends(get_db)) -> BankTransactionRepository:
    return BankTransactionRepository(db)

def get_bank_transaction_service(
        category_repo: BankCategoryRepository = Depends(get_bank_category_repository), 
        account_repo: BankAccountRepository = Depends(get_bank_account_repository), 
        transaction_repo: BankTransactionRepository = Depends(get_bank_transaction_repository)):
    return BankTransactionService(account_repo, transaction_repo, category_repo)
