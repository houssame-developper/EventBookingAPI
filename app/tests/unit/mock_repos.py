from unittest.mock import AsyncMock

import pytest

from repositories.booking_repo import BookingRepo
from repositories.event_repo import EventRepo
from repositories.user_repo import UserRepo


@pytest.fixture
def mock_user_repo() -> UserRepo:
    """Fixture to create a mock UserRepo."""
    mock = AsyncMock(spec=UserRepo)
    return mock


@pytest.fixture
def mock_event_repo() -> EventRepo:
    """Fixture to create a mock EventRepo."""
    mock = AsyncMock(spec=EventRepo)
    return mock


@pytest.fixture
def mock_booking_repo() -> BookingRepo:
    """Fixture to create a mock BookingRepo."""
    mock = AsyncMock(spec=BookingRepo)
    return mock