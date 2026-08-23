from uuid import UUID
from fastapi import HTTPException, status
from pwdlib import PasswordHash
from pwdlib.hashers.bcrypt import BcryptHasher
from jwt import encode,decode,ExpiredSignatureError,InvalidTokenError
from datetime import datetime,timezone,timedelta
from config.settings import SECRET_KEY, TIME_EXPIRE_ACCESS_TOKEN, TIME_EXPIRE_REFRESH_TOKEN
from dataclasses import dataclass
from models import UserRole

@dataclass(slots=True, frozen=True)
class TokenData:
    user_id: UUID
    role: UserRole

    def __post_init__(self) -> None:
        if self.user_id is None or self.role is None:
            raise ValueError("token is corrupted")
        if isinstance(self.user_id, str):
            object.__setattr__(self, "user_id", UUID(self.user_id))
        if isinstance(self.role, str):
            object.__setattr__(self, "role", UserRole(self.role))

    def uuid_to_str(self):
        return str(self.user_id)  
        
    def enum_to_str(self):
        return self.role.value

ctx = PasswordHash((BcryptHasher(),))


def hashing_password(password:str):
    return  ctx.hash(password)

def verify_password(password:str,hash_password:str):
    return ctx.verify(password,hash_password)    


def generate_token(tokenData:TokenData,refresh_token:bool=False) -> str:
    delta = TIME_EXPIRE_ACCESS_TOKEN  if not refresh_token else TIME_EXPIRE_REFRESH_TOKEN
    payload = {
        "user_id":tokenData.uuid_to_str(),
        "role":tokenData.enum_to_str(),
        "exp":datetime.now(timezone.utc) + timedelta(seconds=delta)
    } 
    return encode(payload=payload,key=SECRET_KEY,algorithm="HS256")

def verify_token(token: str) -> TokenData:
    try:
        payload = decode(token, SECRET_KEY, algorithms=["HS256"])
        return TokenData(user_id=payload["user_id"], role=payload["role"])

    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired"
        )
    except (InvalidTokenError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or corrupt token",
        )
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token payload is missing required fields",
        )

import functools


def admin_access_required(func):
    @functools.wraps(func)
    def wrapper(role: UserRole, *args, **kwargs):
        if role.value == "user":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="This page not found",
            )
        return func(role, *args, **kwargs)

    return wrapper