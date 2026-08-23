import pytest
from unittest.mock import AsyncMock
from uuid import uuid4
from datetime import datetime
from fastapi import HTTPException
from service.event_service import EventService

@pytest.fixture(scope="class")
def event_service() -> EventService:
    return EventService()


def make_event(**kwargs):
    """Helper to create a mock event object with default values."""
    defaults = {
        'id': uuid4(),
        'title': 'Test Event',
        'description': 'Test Description',
        'date': datetime.now(),
        'total_slots': 100,
        'reserved_slots': 0,
        'created_at': datetime.now(),
        'updated_at': datetime.now(),
        'deleted_at': None,
    }
    defaults.update(kwargs)
    return type('Event', (), defaults)()


def make_booking(**kwargs):
    """Helper to create a mock booking object with default values."""
    defaults = {
        'id': uuid4(),
        'user_id': uuid4(),
        'event_id': uuid4(),
        'booking_date': datetime.now(),
    }
    defaults.update(kwargs)
    return type('Booking', (), defaults)()


# ==========================================
# Create Event Tests
# ==========================================

async def test_create_event_success(event_service: EventService, mock_event_repo, event_create_factory):
    """Test successful event creation."""
    event_data = event_create_factory.build()
    created_event = make_event(title=event_data.title)

    mock_event_repo.create.return_value = created_event

    result = await event_service.create_event(event_data, mock_event_repo)

    assert result is not None
    assert result.title == event_data.title
    mock_event_repo.create.assert_called_once_with(event_data)


# ==========================================
# Update Event Tests
# ==========================================

async def test_update_event_not_found(event_service: EventService, mock_event_repo, event_update_factory):
    """Test update fails when event does not exist (422)."""
    event_data = event_update_factory.build()
    mock_event_repo.get_by_id.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        await event_service.update_event(uuid4(), event_data, mock_event_repo)

    assert exc_info.value.status_code == 422
    assert "does not exist" in exc_info.value.detail


async def test_update_event_success(event_service: EventService, mock_event_repo, event_update_factory):
    """Test successful event update."""
    event_id = uuid4()
    event_data = event_update_factory.build()
    existing_event = make_event(id=event_id)
    updated_event = make_event(id=event_id, title="Updated Title")

    mock_event_repo.get_by_id.return_value = existing_event
    mock_event_repo.update.return_value = updated_event

    result = await event_service.update_event(event_id, event_data, mock_event_repo)

    assert result is not None
    mock_event_repo.get_by_id.assert_called_once_with(event_id)
    mock_event_repo.update.assert_called_once_with(existing_event, event_data)


# ==========================================
# Delete Event Tests
# ==========================================

async def test_delete_event_not_found(event_service: EventService, mock_event_repo):
    """Test delete fails when event does not exist (422)."""
    mock_event_repo.get_by_id.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        await event_service.delete_event(uuid4(), mock_event_repo)

    assert exc_info.value.status_code == 422
    assert "does not exist" in exc_info.value.detail


async def test_delete_event_success(event_service: EventService, mock_event_repo):
    """Test successful event deletion."""
    event_id = uuid4()
    existing_event = make_event(id=event_id)

    mock_event_repo.get_by_id.return_value = existing_event

    result = await event_service.delete_event(event_id, mock_event_repo)

    assert result is not None
    assert result["message"] == "event deleted successfully"
    mock_event_repo.delete.assert_called_once_with(existing_event)


# ==========================================
# Get Event Tests
# ==========================================

async def test_get_event_not_found(event_service: EventService, mock_event_repo):
    """Test get event fails when event does not exist (422)."""
    mock_event_repo.get_by_id.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        await event_service.get_event(uuid4(), mock_event_repo)

    assert exc_info.value.status_code == 422
    assert "does not exist" in exc_info.value.detail


async def test_get_event_success(event_service: EventService, mock_event_repo):
    """Test successful get event."""
    event_id = uuid4()
    existing_event = make_event(id=event_id)

    mock_event_repo.get_by_id.return_value = existing_event

    result = await event_service.get_event(event_id, mock_event_repo)

    assert result is not None
    assert result.id == event_id
    mock_event_repo.get_by_id.assert_called_once_with(event_id)


# ==========================================
# Get List Event Tests (Pagination)
# ==========================================

async def test_get_list_event_success(event_service: EventService, mock_event_repo):
    """Test successful get list of events with pagination."""
    events = [make_event(), make_event(), make_event()]
    mock_event_repo.get_all_pagination.return_value = events

    result = await event_service.get_list_event(mock_event_repo, current_page=1, page_size=20)

    assert result is not None
    assert len(result) == 3
    mock_event_repo.get_all_pagination.assert_called_once_with(0, 20)


async def test_get_list_event_page_2(event_service: EventService, mock_event_repo):
    """Test pagination calculates offset correctly for page 2."""
    events = [make_event()]
    mock_event_repo.get_all_pagination.return_value = events

    result = await event_service.get_list_event(mock_event_repo, current_page=2, page_size=10)

    assert result is not None
    mock_event_repo.get_all_pagination.assert_called_once_with(10, 10)


# ==========================================
# Get Slots Tests
# ==========================================

async def test_get_slots_success(event_service: EventService, mock_booking_repo):
    """Test successful get slots count."""
    event_id = uuid4()
    mock_booking_repo.count_by_event_id.return_value = 42

    result = await event_service.get_slots(event_id, mock_booking_repo)

    assert result == 42
    mock_booking_repo.count_by_event_id.assert_called_once_with(event_id)


# ==========================================
# Create Booking Tests
# ==========================================

async def test_create_booking_event_not_found(
    event_service: EventService, mock_event_repo, mock_booking_repo
):
    """Test booking fails when event does not exist (422)."""
    mock_event_repo.get_by_id.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        await event_service.create_booking(uuid4(), uuid4(), mock_event_repo, mock_booking_repo)

    assert exc_info.value.status_code == 422
    assert "does not exist" in exc_info.value.detail


async def test_create_booking_no_slots_available(
    event_service: EventService, mock_event_repo, mock_booking_repo
):
    """Test booking fails when no slots available (422)."""
    event_id = uuid4()
    user_id = uuid4()
    event = make_event(id=event_id, total_slots=10, reserved_slots=10)

    mock_event_repo.get_by_id.return_value = event
    mock_booking_repo.count_by_event_id.return_value = 10

    with pytest.raises(HTTPException) as exc_info:
        await event_service.create_booking(event_id, user_id, mock_event_repo, mock_booking_repo)

    assert exc_info.value.status_code == 422
    assert "No slots available" in exc_info.value.detail


async def test_create_booking_success(
    event_service: EventService, mock_event_repo, mock_booking_repo
):
    """Test successful booking creation."""
    event_id = uuid4()
    user_id = uuid4()
    event = make_event(id=event_id, total_slots=100, reserved_slots=5)
    booking = make_booking(user_id=user_id, event_id=event_id)

    mock_event_repo.get_by_id.return_value = event
    mock_booking_repo.count_by_event_id.return_value = 5
    mock_booking_repo.create.return_value = booking

    result = await event_service.create_booking(event_id, user_id, mock_event_repo, mock_booking_repo)

    assert result is not None
    assert result.user_id == user_id
    assert result.event_id == event_id
    mock_booking_repo.create.assert_called_once()
    mock_event_repo.update.assert_called_once()
