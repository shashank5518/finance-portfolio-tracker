from decimal import Decimal

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from config.base import Base


class Budget(Base):
    __tablename__ = "financial_budget"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    category_id: Mapped[int] = mapped_column(ForeignKey("bank_categories.id"), nullable=False)
    budget_allocated: Mapped[Decimal]

    user = relationship("User", back_populates="financial_budget")
    category = relationship("BankCategory", back_populates="financial_budget")