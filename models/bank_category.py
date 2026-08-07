from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from config.base import Base

if TYPE_CHECKING:
    from models.bank_transaction import BankTransaction
    from models.budget import Budget


class BankCategory(Base):
    __tablename__ = "bank_categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(String(255), nullable=False)

    transactions: Mapped[list["BankTransaction"]] = relationship(
        back_populates="category"
    )

    budgets: Mapped[list["Budget"]] = relationship(back_populates="category")