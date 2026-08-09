from fastapi import Depends
from sqlalchemy.orm import Session

from config.database_connection import get_db
from dependencies.user_dependencies import get_user_repository
from repositories.bank_account_repository import BankAccountRepository
from repositories.user_repository import UserRepository
from service.bank_account_service import BankAccountService


def get_bank_account_repository(db: Session  = Depends(get_db)) -> BankAccountRepository:
    return BankAccountRepository(db)

def get_bank_account_service(user_repo: UserRepository = Depends(get_user_repository), bank_account_repo: BankAccountRepository = Depends(get_bank_account_repository)) -> BankAccountService:
    return BankAccountService(user_repo, bank_account_repo)