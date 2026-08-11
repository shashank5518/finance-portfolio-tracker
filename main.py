from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from exceptions.bank_account_exceptions import AccountNotFoundError
from exceptions.bank_transaction_exceptions import (
    CategoryNotFoundError,
    TransactionNotFoundError,
)
from exceptions.demat_account_exceptions import DematAccountNotFoundError
from exceptions.demat_transaction_exceptions import HoldingNotFoundError
from exceptions.user_service_exceptions import UserNotFoundError
from routers.bank_account_router import router as bank_account_router
from routers.bank_transaction_router import router as bank_transaction_router
from routers.demat_account_router import router as demat_account_router
from routers.demat_transaction_router import router as demat_transaction_router
from routers.user_router import router as user_router

app = FastAPI(title="Finance Portfolio Tracker", version="1.0.0")

app.include_router(user_router)
app.include_router(bank_account_router)
app.include_router(bank_transaction_router)
app.include_router(demat_account_router)
app.include_router(demat_transaction_router)


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.exception_handler(UserNotFoundError)
async def user_not_found_handler(request: Request, exc: UserNotFoundError):
    return JSONResponse(
        status_code=404,
        content={"detail": str(exc)},
    )


@app.exception_handler(AccountNotFoundError)
async def account_not_found_handler(request: Request, exc: AccountNotFoundError):
    return JSONResponse(
        status_code=404,
        content={"detail": str(exc)},
    )


@app.exception_handler(CategoryNotFoundError)
async def category_not_found_handler(request: Request, exc: CategoryNotFoundError):
    return JSONResponse(
        status_code=404,
        content={"detail": str(exc)},
    )


@app.exception_handler(TransactionNotFoundError)
async def transaction_not_found_handler(
    request: Request, exc: TransactionNotFoundError
):
    return JSONResponse(
        status_code=404,
        content={"detail": str(exc)},
    )


@app.exception_handler(DematAccountNotFoundError)
async def demat_account_not_found_handler(
    request: Request, exc: DematAccountNotFoundError
):
    return JSONResponse(
        status_code=404,
        content={"detail": str(exc)},
    )

@app.exception_handler(HoldingNotFoundError)
async def holding_not_found_handler(
    request: Request, exc: HoldingNotFoundError
):
    return JSONResponse(
        status_code=404,
        content={"detail": str(exc)},
    )


