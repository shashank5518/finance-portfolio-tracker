from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal


@dataclass(slots=True)
class BankTransactionCreate:
    amount: Decimal
    description: str
    bank_account_id: int
    transaction_type: str
    category_id: int


@dataclass(slots=True)
class BankTransaction:
    id: int
    amount: Decimal
    description: str
    bank_account_id: int
    transaction_timestamp: datetime
    transaction_type: str
    category_id: int
