from fastapi import APIRouter, Depends, status

from dependencies.demat_account_dependencies import get_demat_account_service
from schemas.demat_account import (
    DematAccountCreate,
    DematAccountResponse,
    DematAccountUpdate,
)
from service.demat_account_service import DematAccountService

router = APIRouter(prefix="/demat_accounts", tags=["DematAccounts"])


@router.post(
    "/", response_model=DematAccountResponse, status_code=status.HTTP_201_CREATED
)
def create_account(
    demat_account: DematAccountCreate,
    service: DematAccountService = Depends(get_demat_account_service),
):
    return service.create_account(demat_account)


@router.get("/{account_id}", response_model=DematAccountResponse)
def get_account(
    account_id: int,
    service: DematAccountService = Depends(get_demat_account_service),
):
    return service.get_account_by_id(account_id)


@router.get("/user/{user_id}", response_model=list[DematAccountResponse])
def get_accounts_by_user(
    user_id: int,
    service: DematAccountService = Depends(get_demat_account_service),
):
    return service.get_accounts_by_user(user_id)


@router.put("/{account_id}", response_model=DematAccountResponse)
def update_demat_account(
    account_id: int,
    account_name: DematAccountUpdate,
    service: DematAccountService = Depends(get_demat_account_service),
):
    return service.update_account_name(account_id, account_name.account_name)


@router.delete("/{account_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_account(
    account_id: int,
    service: DematAccountService = Depends(get_demat_account_service),
):
    service.delete_account(account_id)
