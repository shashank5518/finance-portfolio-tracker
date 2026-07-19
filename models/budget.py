from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class BudgetCreate:
    user_id: int
    category_id: int
    monthly_limit: int


class Budget:
    id: int
    user_id: int
    category_id: int
    monthly_limit: int
    created_at: datetime
