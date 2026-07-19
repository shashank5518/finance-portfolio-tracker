from decimal import Decimal

from exceptions.demat_transaction_exceptions import (
    InsufficientSharesError,
    InvalidTransactionTypeError,
    PortfolioNotFoundError,
)
from repositories.demat_portfolio_repository import DematPortfolioRepository
from repositories.demat_transaction_repository import (
    DematTransactionRepository,
    InvestmentTransaction,
    InvestmentTransactionCreate,
)


class DematTransactionService:

    def __init__(
        self,
        transaction_repo: DematTransactionRepository,
        portfolio_repo: DematPortfolioRepository,
    ) -> None:
        self.transaction_repo = transaction_repo
        self.portfolio_repo = portfolio_repo

    def create(
        self, transaction_data: InvestmentTransactionCreate
    ) -> InvestmentTransaction:
        portfolio = self.portfolio_repo.find_by_id(transaction_data.portfolio_id)
        if portfolio is None:
            raise PortfolioNotFoundError(
                f"Portfolio '{transaction_data.portfolio_id}' not found."
            )
        if transaction_data.transaction_type == "sell":
            if portfolio.quantity < transaction_data.quantity:
                raise InsufficientSharesError("Not enough shares.")
            else:
                new_quantity = portfolio.quantity - transaction_data.quantity
                new_average_price = (
                    Decimal("0") if new_quantity == 0 else portfolio.average_buy_price
                )

            self.portfolio_repo.update_position(
                transaction_data.portfolio_id, new_quantity, new_average_price
            )
        elif transaction_data.transaction_type == "buy":
            new_quantity = portfolio.quantity + transaction_data.quantity
            new_average_price = (
                portfolio.quantity * portfolio.average_buy_price
                + transaction_data.quantity * transaction_data.price_per_unit
            ) / new_quantity
            self.portfolio_repo.update_position(
                transaction_data.portfolio_id, new_quantity, new_average_price
            )
        else:
            raise InvalidTransactionTypeError(
                f"Transaction type '{transaction_data.transaction_type}' is invalid."
            )
        transaction = self.transaction_repo.create(transaction_data)
        return transaction
