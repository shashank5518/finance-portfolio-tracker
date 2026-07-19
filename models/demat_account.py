from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class DematAccountCreate:
    user_id: int
    broker_name: str
    account_name: str
    broker_account_id: str


@dataclass(slots=True)
class DematAccount:
    id: int
    user_id: int
    broker_name: str
    account_name: str
    broker_account_id: str
    created_at: datetime
