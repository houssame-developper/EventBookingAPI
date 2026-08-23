from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query, Request

from api.deps import AdminUser, CurrentUser
from config.limiter import DEFAULT_RATE_LIMIT, limiter
from repositories.user_repo import UserRepo
from schemas.user_schema import UserCreate, UserRead, UserUpdate
from service.user_service import UserService

router = APIRouter(prefix="/users", tags=["users"])
user_service = UserService()


@router.post("", response_model=UserRead)
@limiter.limit(DEFAULT_RATE_LIMIT)
async def create_user(
    request: Request,
    user_data: UserCreate,
    _: AdminUser,
    user_repo: Annotated[UserRepo, Depends()],
):  
    user = await user_service.create_user(user_data, user_repo)
    return UserRead.model_validate(user, from_attributes=True)


@router.get("/me", response_model=UserRead)
@limiter.limit(DEFAULT_RATE_LIMIT)
async def get_me(request: Request, current_user: CurrentUser):
    return UserRead.model_validate(current_user, from_attributes=True)


@router.get("", response_model=list[UserRead])
@limiter.limit(DEFAULT_RATE_LIMIT)
async def list_users(
    request: Request,
    _: AdminUser,
    user_repo: Annotated[UserRepo, Depends()],
    current_page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
):
    users = await user_service.get_list_user(user_repo, current_page, page_size)
    return [UserRead.model_validate(u, from_attributes=True) for u in users]


@router.get("/{user_id}", response_model=UserRead)
@limiter.limit(DEFAULT_RATE_LIMIT)
async def get_user(
    request: Request,
    user_id: UUID,
    _: AdminUser,
    user_repo: Annotated[UserRepo, Depends()],
):
    user = await user_service.get_user(user_id, user_repo)
    return UserRead.model_validate(user, from_attributes=True)


@router.patch("/{user_id}", response_model=UserRead)
@limiter.limit(DEFAULT_RATE_LIMIT)
async def update_user(
    request: Request,
    user_id: UUID,
    user_data: UserUpdate,
    _: AdminUser,
    user_repo: Annotated[UserRepo, Depends()],
):
    user = await user_service.update_user(user_id, user_data, user_repo)
    return UserRead.model_validate(user, from_attributes=True)


@router.delete("/{user_id}")
@limiter.limit(DEFAULT_RATE_LIMIT)
async def delete_user(
    request: Request,
    user_id: UUID,
    _: AdminUser,
    user_repo: Annotated[UserRepo, Depends()],
):
    return await user_service.delete_user(user_id, user_repo)
