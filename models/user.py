from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from config.base import Base

if TYPE_CHECKING:
    from models.bank_account import BankAccount
    from models.demat_account import DematAccount


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    bank_accounts: Mapped[list["BankAccount"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )

    demat_accounts: Mapped[list["DematAccount"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
