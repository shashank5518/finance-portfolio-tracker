from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from models.bank_account import Currency


class BankAccountBase(BaseModel):
    bank_name: str
    account_name: str
    account_number: str
    balance: Decimal
    currency: Currency

class BankAccountUpdate(BaseModel):
    account_name: str

class BankAccountCreate(BankAccountBase):
    user_id: int

class BankAccountResponse(BankAccountBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

