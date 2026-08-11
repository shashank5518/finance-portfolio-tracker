from fastapi import APIRouter, Depends

from dependencies.auth_dependencies import get_auth_service
from schemas.auth import LoginRequest, TokenResponse
from service.auth_service import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post("/login", response_model=TokenResponse)
def login(
    credentials: LoginRequest,
    service: AuthService = Depends(get_auth_service),
):
    return service.login(credentials.email, credentials.password)