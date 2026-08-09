from fastapi import APIRouter, Depends, status

from dependencies.user_dependencies import get_user_service
from schemas.user import UserCreate, UserResponse, UserUpdate
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

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED, summary = "Create a new user", description = "Creates a new ser after validating email uniqueness.")
def create_user(
    user: UserCreate,
    service: UserService = Depends(get_user_service),
):
    return service.create_user(user)

@router.put("/{user_id}", response_model=UserResponse,)
def update_user(user_id: int, user: UserUpdate, service: UserService = Depends(get_user_service),):
    return service.update_user(user_id, user)