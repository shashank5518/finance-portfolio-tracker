from decimal import Decimal

from exceptions.demat_transaction_exceptions import (
    HoldingNotFoundError,
    InsufficientSharesError,
    InvalidTransactionTypeError,
)
from models.demat_transaction import TransactionType
from repositories.demat_portfolio_repository import DematHoldingRepository
from repositories.demat_transaction_repository import (
    DematTransaction,
    DematTransactionRepository,
)
from schemas.demat_transaction import DematTransactionCreate


class DematTransactionService:

    def __init__(
        self,
        transaction_repo: DematTransactionRepository,
        holding_repo: DematHoldingRepository,
    ) -> None:
        self.transaction_repo = transaction_repo
        self.holding_repo = holding_repo

    def create_transaction(
        self, transaction_data: DematTransactionCreate
    ) -> DematTransaction:
        holding = self.holding_repo.find_by_id(transaction_data.holding_id)
        if holding is None:
            raise HoldingNotFoundError(
                f"Holding '{transaction_data.holding_id}' not found."
            )
        if transaction_data.quantity <= 0:
            raise ValueError("Quantity must be greater than zero.")

        if transaction_data.price_per_unit <= 0:
            raise ValueError("Price per unit must be greater than zero.")
        if transaction_data.transaction_type == TransactionType.SELL:
            if holding.quantity < transaction_data.quantity:
                raise InsufficientSharesError("Not enough shares.")

            new_quantity = holding.quantity - transaction_data.quantity
            new_average_price = (
                Decimal("0") if new_quantity == 0 else holding.average_buy_price
            )
            holding.quantity = new_quantity
            holding.average_buy_price = new_average_price
        elif transaction_data.transaction_type == TransactionType.BUY:
            new_quantity = holding.quantity + transaction_data.quantity
            new_average_price = (
                holding.quantity * holding.average_buy_price
                + transaction_data.quantity * transaction_data.price_per_unit
            ) / new_quantity
            holding.quantity = new_quantity
            holding.average_buy_price = new_average_price
        else:
            raise InvalidTransactionTypeError(
                f"Transaction type '{transaction_data.transaction_type}' is invalid."
            )
        transaction = DematTransaction(
            holding_id=transaction_data.holding_id,
            transaction_type=transaction_data.transaction_type,
            quantity=transaction_data.quantity,
            price_per_unit=transaction_data.price_per_unit,
            brokerage=transaction_data.brokerage,
        )
        return self.transaction_repo.create(transaction)
