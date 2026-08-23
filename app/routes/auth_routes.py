from typing import Annotated

from fastapi import APIRouter, Cookie, Depends, HTTPException, Request, Response, status

from config.limiter import AUTH_RATE_LIMIT, limiter
from repositories.user_repo import UserRepo
from schemas.user_schema import Login, Register
from service.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])
auth_service = AuthService()


@router.post("/login")
@limiter.limit(AUTH_RATE_LIMIT)
async def login(
    request: Request,
    login_data: Login,
    response: Response,
    user_repo: Annotated[UserRepo, Depends()],
):
    return await auth_service.login(login_data, user_repo, response)

@router.post("/register")
@limiter.limit(AUTH_RATE_LIMIT)
async def register(
    request: Request,
    register_data: Register,
    response: Response,
    user_repo: Annotated[UserRepo, Depends()],
):
    return await auth_service.register(register_data, user_repo, response)


@router.post("/refresh")
@limiter.limit(AUTH_RATE_LIMIT)
async def refresh_access_token(
        request: Request,
        refresh_token: Annotated[str | None, Cookie()] = None,
    ):
        if not refresh_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token missing",
            )
        return auth_service.refresh_access_token(refresh_token)


@router.post("/logout")
async def logout(
        request: Request,
        response: Response,
    ):
    return auth_service.logout(response)
