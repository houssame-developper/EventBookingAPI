import pytest
import uuid
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from models import User, UserRole
from config.auth_utils import generate_token, TokenData, hashing_password


@pytest.fixture
async def admin_user(db_session: AsyncSession) -> User:
    email = f"admin_{uuid.uuid4().hex}@example.com"
    user = User(
        name="Admin User",
        email=email,
        password_hash=hashing_password("adminpass123"),
        role=UserRole.ADMIN,
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


@pytest.fixture
async def regular_user(db_session: AsyncSession) -> User:
    email = f"user_{uuid.uuid4().hex}@example.com"
    user = User(
        name="Regular User",
        email=email,
        password_hash=hashing_password("userpass123"),
        role=UserRole.USER,
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


@pytest.fixture
async def admin_token(admin_user: User) -> str:
    return generate_token(TokenData(user_id=admin_user.id, role=admin_user.role))


@pytest.fixture
async def regular_token(regular_user: User) -> str:
    return generate_token(TokenData(user_id=regular_user.id, role=regular_user.role))


@pytest.fixture
def admin_headers(admin_token: str) -> dict:
    return {"Authorization": f"Bearer {admin_token}"}


@pytest.fixture
def regular_headers(regular_token: str) -> dict:
    return {"Authorization": f"Bearer {regular_token}"}