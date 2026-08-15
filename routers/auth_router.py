from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from dependencies.auth_dependencies import get_auth_service, get_current_user
from models.user import User
from schemas.auth import LoginRequest, TokenResponse
from schemas.user import UserResponse
from service.auth_service import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post("/login", response_model=TokenResponse)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    service: AuthService = Depends(get_auth_service),
):
    return service.login(form_data.username, form_data.password)

@router.get("/me", response_model=UserResponse)
def me(current_user: User = Depends(get_current_user)):
    return current_user