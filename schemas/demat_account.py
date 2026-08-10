from pydantic import BaseModel, ConfigDict


class DematAccountBase(BaseModel):
    broker_name: str
    account_name: str
    broker_account_id: str


class DematAccountCreate(DematAccountBase):
    user_id: int


class DematAccountUpdate(BaseModel):
    account_name: str


class DematAccountResponse(DematAccountBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
