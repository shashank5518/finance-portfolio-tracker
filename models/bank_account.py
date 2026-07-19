from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal


@dataclass(slots=True)
class BankAccountCreate:
    user_id: int
    bank_name: str
    account_name: str
    account_number: str
    balance: Decimal
    currency: str


@dataclass(slots=True)
class BankAccount:
    id: int
    user_id: int
    bank_name: str
    account_name: str
    account_number: str
    balance: Decimal
    currency: str
    created_at: datetime
