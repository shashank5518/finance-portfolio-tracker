from fastapi import APIRouter, Depends, status

from dependencies.auth_dependencies import get_current_user
from dependencies.bank_account_dependencies import get_bank_account_service
from models.user import User
from schemas.bank_account import (
    BankAccountCreate,
    BankAccountResponse,
    BankAccountUpdate,
)
from service.bank_account_service import BankAccountService

router = APIRouter(prefix="/bank_accounts", tags=["BankAccounts"])


@router.post(
    "/",
    response_model=BankAccountResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new bank account",
    description="Creates a new bank account after validating user existence",
)
def create_account(
    bank_account: BankAccountCreate,
    current_user: User = Depends(get_current_user),
    service: BankAccountService = Depends(get_bank_account_service),
):
    return service.create_account(bank_account, current_user.id)


@router.get("/me", response_model=list[BankAccountResponse])
def get_my_accounts(
    current_user: User = Depends(get_current_user),
    service: BankAccountService = Depends(get_bank_account_service),
):
    return service.get_accounts_by_user(current_user.id)


@router.get("/{account_id}", response_model=BankAccountResponse)
def get_account(
    account_id: int,
    current_user: User = Depends(get_current_user),
    service: BankAccountService = Depends(get_bank_account_service),
):
    return service.get_account_by_id(account_id, current_user)


# @router.get("/users/{user_id}", response_model=list[BankAccountResponse])
# def get_accounts_by_user_id(
#     user_id: int,
#     service: BankAccountService = Depends(get_bank_account_service),
# ):
#     return service.get_accounts_by_user(user_id)


@router.put("/{account_id}", response_model=BankAccountResponse)
def update_account_name(
    account_id: int,
    account_name: BankAccountUpdate,
    current_user: User = Depends(get_current_user),
    service: BankAccountService = Depends(get_bank_account_service),
):
    return service.update_account_name(
        account_id, current_user, account_name.account_name
    )


@router.delete("/{account_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_bank_account(
    account_id: int,
    current_user: User = Depends(get_current_user),
    service: BankAccountService = Depends(get_bank_account_service),
):
    service.delete_account(account_id, current_user)
