from collections.abc import Sequence

from exceptions.demat_account_exceptions import (
    DematAccountNotFoundError,
    DuplicateBrokerAccountIdError,
)
from exceptions.user_service_exceptions import UserNotFoundError
from repositories.demat_account_repository import (
    DematAccount,
    DematAccountRepository,
)
from repositories.user_repository import UserRepository
from schemas.demat_account import DematAccountCreate

class DematAccountService:
    def __init__(
        self, demat_acc_repo: DematAccountRepository, user_repo: UserRepository
    ) -> None:
        self.demat_acc_repo = demat_acc_repo
        self.user_repo = user_repo

    def create_account(self, account_data: DematAccountCreate) -> DematAccount:
        user = self.user_repo.find_by_id(account_data.user_id)
        if user is None:
            raise UserNotFoundError(f"User '{account_data.user_id}' not found.")
        if self.demat_acc_repo.exists_by_broker_account_id(
            account_data.broker_account_id
        ):
            raise DuplicateBrokerAccountIdError(
                f"Broker account '{account_data.broker_account_id}' already exists."
            )
        demat_account = DematAccount(
            user_id = account_data.user_id,
            broker_name = account_data.broker_name,
            account_name = account_data.account_name,
            broker_account_id = account_data.broker_account_id
        )
        return self.demat_acc_repo.create(demat_account)

    def get_account_by_id(self, account_id: int) -> DematAccount:
        account = self.demat_acc_repo.find_by_id(account_id)
        if account is None:
            raise DematAccountNotFoundError(
                f"Demat account '{account_id}' does not exist."
            )
        return account

    def get_accounts_by_user(self, user_id: int) -> Sequence[DematAccount]:
        user = self.user_repo.find_by_id(user_id)
        if user is None:
            raise UserNotFoundError(f"User '{user_id}' not found.")
        return self.demat_acc_repo.find_all_by_user(user_id)

    def update_account_name(self, account_id: int, new_name: str) -> DematAccount:
        updated_account = self.demat_acc_repo.update_account_name(account_id, new_name)
        if updated_account is None:
            raise DematAccountNotFoundError(
                f"Demat account '{account_id}' does not exist."
            )
        return updated_account

    def delete_account(self, account_id: int) -> None:
        deleted = self.demat_acc_repo.delete(account_id)
        if not deleted:
            raise DematAccountNotFoundError(
                f"Demat account '{account_id}' does not exist."
            )
