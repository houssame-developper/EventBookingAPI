import pytest
from unittest.mock import AsyncMock
from uuid import uuid4, UUID
from datetime import datetime
from fastapi import HTTPException
from config.auth_utils import hashing_password, TokenData, generate_token
from models import UserRole
from service.auth_service import AuthService

@pytest.fixture(scope="class")
def auth_service() -> AuthService:
    return AuthService()


@pytest.fixture
def mock_user_repo() -> AsyncMock:
    return AsyncMock()


def make_user(**kwargs):
    """Helper to create a mock user object with default values."""
    defaults = {
        'id': uuid4(),
        'name': 'Test User',
        'email': 'test@example.com',
        'role': UserRole.USER,
        'created_at': datetime.now(),
        'updated_at': datetime.now(),
        'deleted_at': None,
    }
    defaults.update(kwargs)
    return type('User', (), defaults)()


# ==========================================
# Register Tests
# ==========================================

async def test_invalid_register_email_exists(auth_service: AuthService, mock_user_repo, response_mock, register_factory):
    """Test register fails when email already exists (422)."""
    register_data = register_factory.build()

    mock_user_repo.get_by_email.return_value = make_user(email=register_data.email)

    with pytest.raises(HTTPException) as exc_info:
        await auth_service.register(register_data, mock_user_repo, response_mock)

    assert exc_info.value.status_code == 422
    assert "exists" in exc_info.value.detail


async def test_invalid_register_empty_user(auth_service: AuthService, mock_user_repo, response_mock, register_factory):
    """Test register fails when create returns None/empty (422)."""
    register_data = register_factory.build()

    mock_user_repo.get_by_email.return_value = None
    mock_user_repo.create.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        await auth_service.register(register_data, mock_user_repo, response_mock)

    assert exc_info.value.status_code == 422
    assert "empty" in exc_info.value.detail


async def test_valid_register(auth_service: AuthService, mock_user_repo, response_mock, register_factory):
    """Test successful registration."""
    register_data = register_factory.build()

    mock_user_repo.get_by_email.return_value = None
    mock_user_repo.create.return_value = make_user(
        name=register_data.name,
        email=register_data.email,
    )

    user_data = await auth_service.register(register_data, mock_user_repo, response_mock)

    assert user_data is not None
    assert "access_token" in user_data
    assert "user" in user_data
    assert response_mock.set_cookie.called


# ==========================================
# Login Tests
# ==========================================

async def test_invalid_login_email_not_found(auth_service: AuthService, mock_user_repo, response_mock, login_factory):
    """Test login fails when email does not exist (422)."""
    login_data = login_factory.build()

    mock_user_repo.get_by_email.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        await auth_service.login(login_data, mock_user_repo, response_mock)

    assert exc_info.value.status_code == 422
    assert "not exists" in exc_info.value.detail


async def test_invalid_login_user_deleted(auth_service: AuthService, mock_user_repo, response_mock, login_factory):
    """Test login fails when user is deleted (403)."""
    login_data = login_factory.build()

    mock_user_repo.get_by_email.return_value = make_user(
        email=login_data.email,
        deleted_at=datetime.now(),
    )

    with pytest.raises(HTTPException) as exc_info:
        await auth_service.login(login_data, mock_user_repo, response_mock)

    assert exc_info.value.status_code == 403
    assert "deleted" in exc_info.value.detail


async def test_invalid_login_wrong_password(auth_service: AuthService, mock_user_repo, response_mock, login_factory):
    """Test login fails when password is incorrect (401)."""
    login_data = login_factory.build()

    mock_user_repo.get_by_email.return_value = make_user(
        email=login_data.email,
        password_hash=hashing_password("correct_password"),
    )

    with pytest.raises(HTTPException) as exc_info:
        await auth_service.login(login_data, mock_user_repo, response_mock)

    assert exc_info.value.status_code == 401
    assert "password is not correct" in exc_info.value.detail


async def test_valid_login(auth_service: AuthService, mock_user_repo, response_mock, login_factory):
    """Test successful login."""
    login_data = login_factory.build()
    password_hash = hashing_password(login_data.password)

    mock_user_repo.get_by_email.return_value = make_user(
        email=login_data.email,
        password_hash=password_hash,
    )

    user_data = await auth_service.login(login_data, mock_user_repo, response_mock)

    assert user_data is not None
    assert "access_token" in user_data
    assert "user" in user_data
    assert response_mock.set_cookie.called


# ==========================================
# Refresh Token Tests
# ==========================================

def test_valid_refresh_access_token(auth_service: AuthService):
    """Test successful token refresh."""
    token_data = TokenData(user_id=uuid4(), role=UserRole.ADMIN)
    refresh_token = generate_token(token_data, refresh_token=True)

    data = auth_service.refresh_access_token(refresh_token)

    assert "access_token" in data


def test_invalid_refresh_access_token_tampered(auth_service: AuthService):
    """Test refresh fails with invalid/tampered token (401)."""
    with pytest.raises(HTTPException) as exc_info:
        auth_service.refresh_access_token("invalid_token_here")

    assert exc_info.value.status_code == 401


def test_invalid_refresh_access_token_expired(auth_service: AuthService):
    """Test refresh fails with expired token (401)."""
    from datetime import timedelta
    from jwt import encode
    from config.settings import SECRET_KEY

    expired_payload = {
        "user_id": str(uuid4()),
        "role": "admin",
        "exp": datetime.now() - timedelta(seconds=10),
    }
    expired_token = encode(expired_payload, SECRET_KEY, algorithm="HS256")

    with pytest.raises(HTTPException) as exc_info:
        auth_service.refresh_access_token(expired_token)

    assert exc_info.value.status_code == 401