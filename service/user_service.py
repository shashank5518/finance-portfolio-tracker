from exceptions.user_service_exceptions import (
    DeletionFailedError,
    DuplicateEmailError,
    UpdateFailedError,
    UserNotFoundError,
)
from repositories.user_repository import User, UserCreate, UserRepository


class UserService:

    def __init__(self, user_repo: UserRepository) -> None:
        self.user_repo = user_repo

    def create_user(self, user_data: UserCreate) -> User:
        if self.user_repo.exists_by_email(user_data.email):
            raise DuplicateEmailError(f"Email '{user_data.email}' already exists.")
        return self.user_repo.create(user_data)

    def get_user_by_id(self, user_id: int) -> User:
        user = self.user_repo.find_by_id(user_id)
        if user is None:
            raise UserNotFoundError(f"User '{user_id}' not found.")
        return user

    def get_all_users(self) -> list[User]:
        return self.user_repo.find_all()

    def update_user(self, user_id: int, new_name: str) -> User:
        self.get_user_by_id(user_id)
        updated_user = self.user_repo.update_name(user_id, new_name)
        if updated_user is None:
            raise UpdateFailedError(f"User '{user_id}' was not updated.")
        return updated_user

    def delete_user(self, user_id: int) -> None:
        self.get_user_by_id(user_id)
        deleted = self.user_repo.delete(user_id)
        if deleted is False:
            raise DeletionFailedError("Delete failed.")
