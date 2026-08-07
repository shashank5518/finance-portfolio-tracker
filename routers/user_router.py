from fastapi import APIRouter, Depends, status

from dependencies.user_dependencies import get_user_service
from schemas.user import UserCreate, UserResponse
from service.user_service import UserService

router = APIRouter(
    prefix = "/users",
    tags = ["Users"],
)

@router.get("/", response_model=list[UserResponse])
def get_users(service: UserService = Depends(get_user_service)):
    return service.get_all_users()

@router.get("/{user_id}", response_model=UserResponse)
def get_user_by_id(user_id: int, service: UserService = Depends(get_user_service)):
    return service.get_user_by_id(user_id)

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED,)
def create_user(
    user: UserCreate,
    service: UserService = Depends(get_user_service),
):
    return service.create_user(user)