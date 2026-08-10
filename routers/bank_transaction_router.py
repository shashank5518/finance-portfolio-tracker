from fastapi import APIRouter, Depends, status

from dependencies.bank_transaction_dependencies import get_bank_transaction_service
from schemas.bank_transaction import BankTransactionCreate, BankTransactionResponse
from service.bank_transaction_service import BankTransactionService

router = APIRouter(prefix="/bank_transactions", tags=["BankTransactions"])


@router.post(
    "/",
    response_model=BankTransactionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new bank transaction",
    description="Creates a new bank transaction and updates bank account data",
)
def create_transaction(
    bank_transaction: BankTransactionCreate,
    service: BankTransactionService = Depends(get_bank_transaction_service),
):
    return service.create_transaction(bank_transaction)


@router.get(
    "/recent",
    response_model=list[BankTransactionResponse],
)
def get_recent_transactions(
    service: BankTransactionService = Depends(get_bank_transaction_service),
):
    return service.get_recent_transactions()


@router.get("/{transaction_id}", response_model=BankTransactionResponse)
def get_transaction_by_id(
    transaction_id: int,
    service: BankTransactionService = Depends(get_bank_transaction_service),
):
    return service.get_transaction_by_id(transaction_id)


@router.get("/account/{account_id}", response_model=list[BankTransactionResponse])
def get_transaction_by_account(
    account_id: int,
    service: BankTransactionService = Depends(get_bank_transaction_service),
):
    return service.get_transactions_by_account(account_id)


@router.get("/category/{category_id}", response_model=list[BankTransactionResponse])
def get_transaction_by_category(
    category_id: int,
    service: BankTransactionService = Depends(get_bank_transaction_service),
):
    return service.get_transactions_by_category(category_id)
