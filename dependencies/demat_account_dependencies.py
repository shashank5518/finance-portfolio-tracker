from fastapi import Depends
from sqlalchemy.orm import Session

from config.database_connection import get_db
from dependencies.user_dependencies import get_user_repository
from repositories.demat_account_repository import DematAccountRepository
from repositories.user_repository import UserRepository
from service.demat_account_service import DematAccountService


def get_demat_account_repository(db: Session = Depends(get_db)) -> DematAccountRepository:
    return DematAccountRepository(db)

def get_demat_account_service(user_repo: UserRepository = Depends(get_user_repository), demat_account_repo: DematAccountRepository = Depends(get_demat_account_repository)) -> DematAccountService:
    return DematAccountService(demat_account_repo, user_repo)