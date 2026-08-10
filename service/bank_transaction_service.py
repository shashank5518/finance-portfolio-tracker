from collections.abc import Sequence

from exceptions.bank_account_exceptions import AccountNotFoundError
from exceptions.bank_transaction_exceptions import (
    CategoryNotFoundError,
    InsufficientFundsError,
    TransactionNotFoundError,
)
from models.bank_transaction import TransactionType
from repositories.bank_account_repository import BankAccountRepository
from repositories.bank_category_repository import BankCategoryRepository
from repositories.bank_transaction_repository import (
    BankTransaction,
    BankTransactionRepository,
)
from schemas.bank_transaction import BankTransactionCreate


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
        if transaction_data.amount <= 0:
            raise ValueError("Transaction amount must be greater than zero.")
        elif transaction_data.transaction_type == TransactionType.CREDIT:
            new_balance = account.balance + transaction_data.amount
        elif transaction_data.transaction_type == TransactionType.DEBIT:
            if account.balance < transaction_data.amount:
                raise InsufficientFundsError(
                    f"Account '{account.id}' has insufficient funds."
                )
            new_balance = account.balance - transaction_data.amount
        else:
            raise ValueError(
                f"Unsupported transaction type: {transaction_data.transaction_type}"
            )
        account.balance = new_balance
        transaction = BankTransaction(
            amount=transaction_data.amount,
            description=transaction_data.description,
            transaction_type=transaction_data.transaction_type,
            bank_account_id=transaction_data.bank_account_id,
            category_id=transaction_data.category_id,
        )
        return self.transaction_repo.create(transaction)

    def get_transaction_by_id(self, transaction_id: int) -> BankTransaction:
        transaction = self.transaction_repo.find_by_id(transaction_id)
        if transaction is None:
            raise TransactionNotFoundError(f"Transaction '{transaction_id}' not found")
        return transaction

    def get_transactions_by_account(self, account_id: int) -> Sequence[BankTransaction]:
        account = self.account_repo.find_by_id(account_id)
        if account is None:
            raise AccountNotFoundError(f"Account '{account_id}' not found.")
        return self.transaction_repo.find_by_account_id(account_id)

    def get_transactions_by_category(
        self, category_id: int
    ) -> Sequence[BankTransaction]:
        category = self.category_repo.find_by_id(category_id)
        if category is None:
            raise CategoryNotFoundError(f"Category '{category_id}' not found.")
        return self.transaction_repo.find_by_category_id(category_id)

    def get_recent_transactions(self, limit: int = 10) -> Sequence[BankTransaction]:
        return self.transaction_repo.find_recent_transactions(limit)
