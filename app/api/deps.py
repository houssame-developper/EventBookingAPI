from typing import Annotated
from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from config.auth_utils import TokenData, verify_token
from models import User, UserRole
from repositories.user_repo import UserRepo

bearer_scheme = HTTPBearer(auto_error=True)


async def get_token_data(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(bearer_scheme)],
) -> TokenData:
    return verify_token(credentials.credentials)


async def get_current_user(
    token_data: Annotated[TokenData, Depends(get_token_data)],
    user_repo: Annotated[UserRepo, Depends()],
) -> User:
    user = await user_repo.get_by_id(token_data.user_id)
    if user is None or user.deleted_at is not None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive",
        )
    return user


async def require_admin(
    token_data: Annotated[TokenData, Depends(get_token_data)],
    
) -> TokenData:
    if token_data.role == UserRole.USER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )
    return token_data


CurrentUser = Annotated[User, Depends(get_current_user)]
AdminUser = Annotated[TokenData, Depends(require_admin)]
