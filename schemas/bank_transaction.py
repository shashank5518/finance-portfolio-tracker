from decimal import Decimal

from pydantic import BaseModel, ConfigDict

from models.bank_transaction import TransactionType


class BankTransactionBase(BaseModel):
    amount: Decimal
    description: str
    transaction_type: TransactionType

class BankTransactionCreate(BankTransactionBase):
    bank_account_id: int
    category_id: int

class BankTransactionResponse(BankTransactionBase):
    id: int
    model_config = ConfigDict(from_attributes=True)