from dataclasses import dataclass
from decimal import Decimal


@dataclass(slots=True)
class PortfolioCreate:
    demat_account_id: int
    ticker: str
    asset_name: str
    asset_type: str
    quantity: Decimal
    average_buy_price: Decimal


@dataclass(slots=True)
class Portfolio:
    id: int
    demat_account_id: int
    ticker: str
    asset_name: str
    asset_type: str
    quantity: Decimal
    average_buy_price: Decimal
