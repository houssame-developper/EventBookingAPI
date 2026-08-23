import pytest
from unittest.mock import AsyncMock
from uuid import uuid4
from datetime import datetime
from fastapi import HTTPException
from models import UserRole
from service.user_service import UserService

@pytest.fixture(scope="class")
def user_service() -> UserService:
    return UserService()


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
# Create User Tests
# ==========================================

async def test_create_user_email_exists(user_service: UserService, mock_user_repo, user_create_factory):
    """Test create user fails when email already exists (422)."""
    user_data = user_create_factory.build()
    mock_user_repo.get_by_email.return_value = make_user(email=user_data.email)

    with pytest.raises(HTTPException) as exc_info:
        await user_service.create_user(user_data, mock_user_repo)

    assert exc_info.value.status_code == 422
    assert "already exists" in exc_info.value.detail


async def test_create_user_success(user_service: UserService, mock_user_repo, user_create_factory):
    """Test successful user creation."""
    user_data = user_create_factory.build()
    mock_user_repo.get_by_email.return_value = None
    mock_user_repo.create.return_value = make_user(
        name=user_data.name,
        email=user_data.email,
    )

    result = await user_service.create_user(user_data, mock_user_repo)

    assert result is not None
    assert result.name == user_data.name
    assert result.email == user_data.email
    mock_user_repo.create.assert_called_once_with(user_data)


# ==========================================
# Update User Tests
# ==========================================

async def test_update_user_not_found(user_service: UserService, mock_user_repo, user_update_factory):
    """Test update fails when user does not exist (422)."""
    user_data = user_update_factory.build()
    mock_user_repo.get_by_id.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        await user_service.update_user(uuid4(), user_data, mock_user_repo)

    assert exc_info.value.status_code == 422
    assert "not exists" in exc_info.value.detail


async def test_update_user_success(user_service: UserService, mock_user_repo, user_update_factory):
    """Test successful user update."""
    user_id = uuid4()
    user_data = user_update_factory.build()
    existing_user = make_user(id=user_id)
    updated_user = make_user(id=user_id, name="Updated Name")

    mock_user_repo.get_by_id.return_value = existing_user
    mock_user_repo.update.return_value = updated_user

    result = await user_service.update_user(user_id, user_data, mock_user_repo)

    assert result is not None
    mock_user_repo.get_by_id.assert_called_once_with(user_id)
    mock_user_repo.update.assert_called_once_with(existing_user, user_data)


# ==========================================
# Delete User Tests
# ==========================================

async def test_delete_user_not_found(user_service: UserService, mock_user_repo):
    """Test delete fails when user does not exist (422)."""
    mock_user_repo.get_by_id.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        await user_service.delete_user(uuid4(), mock_user_repo)

    assert exc_info.value.status_code == 422
    assert "not exists" in exc_info.value.detail


async def test_delete_user_success(user_service: UserService, mock_user_repo):
    """Test successful user deletion."""
    user_id = uuid4()
    existing_user = make_user(id=user_id)

    mock_user_repo.get_by_id.return_value = existing_user

    result = await user_service.delete_user(user_id, mock_user_repo)

    assert result is not None
    assert result["message"] == "user deleted successfully"
    mock_user_repo.delete.assert_called_once_with(existing_user)


# ==========================================
# Get User Tests
# ==========================================

async def test_get_user_not_found(user_service: UserService, mock_user_repo):
    """Test get user fails when user does not exist (422)."""
    mock_user_repo.get_by_id.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        await user_service.get_user(uuid4(), mock_user_repo)

    assert exc_info.value.status_code == 422
    assert "not exists" in exc_info.value.detail


async def test_get_user_success(user_service: UserService, mock_user_repo):
    """Test successful get user."""
    user_id = uuid4()
    existing_user = make_user(id=user_id)

    mock_user_repo.get_by_id.return_value = existing_user

    result = await user_service.get_user(user_id, mock_user_repo)

    assert result is not None
    assert result.id == user_id
    mock_user_repo.get_by_id.assert_called_once_with(user_id)


# ==========================================
# Get List User Tests (Pagination)
# ==========================================

async def test_get_list_user_success(user_service: UserService, mock_user_repo):
    """Test successful get list of users with pagination."""
    users = [make_user(), make_user(), make_user()]
    mock_user_repo.get_all_pagination.return_value = users

    result = await user_service.get_list_user(mock_user_repo, current_page=1, page_size=20)

    assert result is not None
    assert len(result) == 3
    mock_user_repo.get_all_pagination.assert_called_once_with(0, 20)


async def test_get_list_user_page_2(user_service: UserService, mock_user_repo):
    """Test pagination calculates offset correctly for page 2."""
    users = [make_user()]
    mock_user_repo.get_all_pagination.return_value = users

    result = await user_service.get_list_user(mock_user_repo, current_page=2, page_size=10)

    assert result is not None
    mock_user_repo.get_all_pagination.assert_called_once_with(10, 10)
