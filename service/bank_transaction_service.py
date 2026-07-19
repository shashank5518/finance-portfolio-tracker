from exceptions.bank_account_exceptions import AccountNotFoundError
from exceptions.bank_transaction_exceptions import (
    CategoryNotFoundError,
    InsufficientFundsError,
    TransactionNotFoundError,
)
from exceptions.user_service_exceptions import UpdateFailedError
from repositories.bank_account_repository import BankAccountRepository
from repositories.bank_category_repository import BankCategoryRepository
from repositories.bank_transaction_repository import (
    BankTransaction,
    BankTransactionCreate,
    BankTransactionRepository,
)


class BankTransactionService:

    def __init__(
        self,
        account_repo: BankAccountRepository,
        transaction_repo: BankTransactionRepository,
        category_repo: BankCategoryRepository,
    ) -> None:
        self.account_repo = account_repo
        self.transaction_repo = transaction_repo
        self.category_repo = category_repo

    def create_transaction(
        self, transaction_data: BankTransactionCreate
    ) -> BankTransaction:
        account = self.account_repo.find_by_id(transaction_data.bank_account_id)
        if account is None:
            raise AccountNotFoundError(
                f"Account '{transaction_data.bank_account_id}' not found."
            )
        category = self.category_repo.find_by_id(transaction_data.category_id)
        if category is None:
            raise CategoryNotFoundError(
                f"Category '{transaction_data.category_id}' not found."
            )
        if transaction_data.transaction_type == "credit":
            new_balance = account.balance + transaction_data.amount
        else:
            if account.balance < transaction_data.amount:
                raise InsufficientFundsError(
                    f"Account '{account.id}' has insufficient funds."
                )
            new_balance = account.balance - transaction_data.amount
        updated = self.account_repo.update_balance(account.account_number, new_balance)
        if updated is None:
            raise UpdateFailedError(
                f"Failed to update balance for account '{account.id}'."
            )
        return self.transaction_repo.create(transaction_data)

    def get_transaction_by_id(self, transaction_id: int) -> BankTransaction:
        transaction = self.transaction_repo.find_by_id(transaction_id)
        if transaction is None:
            raise TransactionNotFoundError(f"Transaction '{transaction_id}' not found.")
        return transaction

    def get_transactions_by_account(self, account_id: int) -> list[BankTransaction]:
        account = self.account_repo.find_by_id(account_id)
        if account is None:
            raise AccountNotFoundError(f"Account '{account_id}' not found.")
        return self.transaction_repo.find_by_account_id(account_id)

    def get_transactions_by_category(self, category_id: int) -> list[BankTransaction]:
        category = self.category_repo.find_by_id(category_id)
        if category is None:
            raise CategoryNotFoundError(f"Category '{category_id}' not found.")
        return self.transaction_repo.find_by_category_id(category_id)

    def get_recent_transactions(self, limit: int = 10) -> list[BankTransaction]:
        return self.transaction_repo.find_recent_transactions(limit)
