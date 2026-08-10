from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from config.base import Base

if TYPE_CHECKING:
    from models.bank_category import BankCategory
    from models.user import User


class Budget(Base):
    __tablename__ = "financial_budget"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    category_id: Mapped[int] = mapped_column(
        ForeignKey("bank_categories.id"), nullable=False
    )
    budget_allocated: Mapped[Decimal]

    user: Mapped["User"] = relationship(back_populates="budgets")
    category: Mapped["BankCategory"] = relationship(back_populates="budgets")
