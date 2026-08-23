import pytest
from uuid import UUID
from models import User, UserRole, Event, Booking
from repositories.user_repo import UserRepo
from repositories.event_repo import EventRepo
from repositories.booking_repo import BookingRepo
from sqlalchemy.ext.asyncio import AsyncSession
from tests.constants import user_create_factory, user_update_factory, event_create_factory, event_update_factory, booking_create_factory,TestUserCreateFactory  

@pytest.fixture(scope="function")
def repo(self, db_session: AsyncSession):
    return BookingRepo(db_session)

@pytest.fixture(scope="function")
def user_repo(self, db_session: AsyncSession):
    return UserRepo(db_session)

@pytest.fixture(scope="function")
def event_repo(self, db_session: AsyncSession):
    return EventRepo(db_session)

    async def test_create_booking(self, repo: BookingRepo, user_repo: UserRepo, event_repo: EventRepo,user_create_factory:TestUserCreateFactory):
        user_data = user_create_factory.build()
        user = await user_repo.create(user_data)

        event_data = event_create_factory.build()
        event_data.total_slots = 10
        event = await event_repo.create(event_data)

        booking_data = booking_create_factory.build()
        booking_data.user_id = user.id
        booking_data.event_id = event.id
        booking = await repo.create(booking_data)
        assert booking.id is not None
        assert booking.user_id == user.id
        assert booking.event_id == event.id

    async def test_count_by_event_id(self, repo: BookingRepo, user_repo: UserRepo, event_repo: EventRepo,user_create_factory):
        user_data = user_create_factory.build()
        user = await user_repo.create(user_data)

        event_data = event_create_factory.build()
        event_data.total_slots = 10
        event = await event_repo.create(event_data)

        for _ in range(3):
            booking_data = booking_create_factory.build()
            booking_data.user_id = user.id
            booking_data.event_id = event.id
            await repo.create(booking_data)

        count = await repo.count_by_event_id(event.id)
        assert count == 3

    async def test_get_by_user_id(self, repo: BookingRepo, user_repo: UserRepo, event_repo: EventRepo,user_create_factory):
        user_data = user_create_factory.build()
        user = await user_repo.create(user_data)

        event_data = event_create_factory.build()
        event_data.total_slots = 10
        event = await event_repo.create(event_data)

        for _ in range(3):
            booking_data = booking_create_factory.build()
            booking_data.user_id = user.id
            booking_data.event_id = event.id
            await repo.create(booking_data)

        bookings = await repo.get_by_user_id(user.id)
        assert len(bookings) == 3
        for b in bookings:
            assert b.user_id == user.id