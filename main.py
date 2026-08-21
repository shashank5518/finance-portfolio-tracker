from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from exceptions.auth_exceptions import InvalidCredentialsError
from exceptions.bank_account_exceptions import (
    AccountNotFoundError,
    DuplicateAccountNumberError,
    ForbiddenError,
)
from exceptions.bank_transaction_exceptions import (
    CategoryNotFoundError,
    InsufficientFundsError,
    TransactionNotFoundError,
)
from exceptions.demat_account_exceptions import DematAccountNotFoundError
from exceptions.demat_transaction_exceptions import (
    HoldingNotFoundError,
    InsufficientSharesError,
    InvalidTransactionTypeError,
)
from exceptions.user_service_exceptions import (
    DuplicateEmailError,
    DuplicatePhoneError,
    UserNotFoundError,
)
from routers.auth_router import router as auth_router
from routers.bank_account_router import router as bank_account_router
from routers.bank_transaction_router import router as bank_transaction_router
from routers.demat_account_router import router as demat_account_router
from routers.demat_transaction_router import router as demat_transaction_router
from routers.user_router import router as user_router

app = FastAPI(title="Finance Portfolio Tracker", version="1.0.0")

app.include_router(auth_router)

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
async def holding_not_found_handler(request: Request, exc: HoldingNotFoundError):
    return JSONResponse(
        status_code=404,
        content={"detail": str(exc)},
    )


@app.exception_handler(DuplicateEmailError)
async def duplicate_email_handler(request: Request, exc: DuplicateEmailError):
    return JSONResponse(
        status_code=409,
        content={"detail": str(exc)},
    )


@app.exception_handler(DuplicatePhoneError)
async def duplicate_phone_handler(request: Request, exc: DuplicatePhoneError):
    return JSONResponse(
        status_code=409,
        content={"detail": str(exc)},
    )


@app.exception_handler(DuplicateAccountNumberError)
async def duplicate_account_number_handler(
    request: Request, exc: DuplicateAccountNumberError
):
    return JSONResponse(
        status_code=409,
        content={"detail": str(exc)},
    )


@app.exception_handler(InsufficientFundsError)
async def insufficient_funds_handler(request: Request, exc: InsufficientFundsError):
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc)},
    )


@app.exception_handler(InsufficientSharesError)
async def insufficient_shares_handler(request: Request, exc: InsufficientSharesError):
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc)},
    )


@app.exception_handler(InvalidTransactionTypeError)
async def invalid_transaction_type_handler(
    request: Request, exc: InvalidTransactionTypeError
):
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc)},
    )


@app.exception_handler(InvalidCredentialsError)
async def invalid_credentials_handler(request: Request, exc: InvalidCredentialsError):
    return JSONResponse(
        status_code=401,
        content={"detail": str(exc)},
    )


@app.exception_handler(ForbiddenError)
async def forbidden_access_handler(request: Request, exc: ForbiddenError):
    return JSONResponse(
        status_code=403,
        content={"detail": str(exc)},
    )
