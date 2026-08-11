from decimal import Decimal

from pydantic import BaseModel, ConfigDict

from models.demat_transaction import TransactionType


class DematTransactionBase(BaseModel):
    transaction_type: TransactionType
    quantity: Decimal
    price_per_unit: Decimal
    brokerage: Decimal

class DematTransactionCreate(DematTransactionBase):
    holding_id: int

class DematTransactionResponse(DematTransactionBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
