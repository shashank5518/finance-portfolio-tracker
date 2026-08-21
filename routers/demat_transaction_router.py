from fastapi import APIRouter, Depends, status

from dependencies.demat_transaction_dependencies import get_demat_transaction_service
from schemas.demat_transaction import DematTransactionCreate, DematTransactionResponse
from service.demat_transaction_service import DematTransactionService

router = APIRouter(prefix="/demat_transactions", tags=["DematTransactions"])


@router.post(
    "/", response_model=DematTransactionResponse, status_code=status.HTTP_201_CREATED
)
def create_account(
    demat_transaction: DematTransactionCreate,
    service: DematTransactionService = Depends(get_demat_transaction_service),
):
    return service.create_transaction(demat_transaction)
