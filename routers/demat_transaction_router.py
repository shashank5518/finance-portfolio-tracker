from fastapi import APIRouter, status, Depends
from schemas.demat_transaction import DematTransactionResponse, DematTransactionCreate
from service.demat_transaction_service import DematTransactionService
from dependencies.demat_transaction_dependencies import get_demat_transaction_service

router = APIRouter(
    prefix="/demat_transactions",
    tags = ["DematTransactions"]
)

@router.post("/", response_model=DematTransactionResponse, status_code=status.HTTP_201_CREATED)
def create_account(demat_transaction: DematTransactionCreate, service: DematTransactionService = Depends(get_demat_transaction_service)):
    return service.create_transaction(demat_transaction)
