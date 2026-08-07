from fastapi import Depends
from sqlalchemy.orm import Session

from config.database_connection import get_db
from repositories.user_repository import UserRepository
from service.user_service import UserService


def get_user_repository(db: Session = Depends(get_db)) -> UserRepository:
    return UserRepository(db)

def get_user_service(repo: UserRepository = Depends(get_user_repository)) -> UserService:
    return UserService(repo)
    