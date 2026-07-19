from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal


@dataclass(slots=True)
class InvestmentTransactionCreate:
    portfolio_id: int
    transaction_type: str
    quantity: Decimal
    price_per_unit: Decimal
    brokerage: Decimal


@dataclass(slots=True)
class InvestmentTransaction:
    id: int
    portfolio_id: int
    transaction_type: str
    quantity: Decimal
    price_per_unit: Decimal
    brokerage: Decimal
    transaction_time: datetime
