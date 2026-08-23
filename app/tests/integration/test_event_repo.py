import pytest
from uuid import UUID
from models import  Event
from repositories.event_repo import EventRepo
from sqlalchemy.ext.asyncio import AsyncSession
from tests.constants import event_create_factory, event_update_factory


@pytest.fixture(scope="function")
def repo(db_session: AsyncSession):
        return EventRepo(db_session)

async def test_create_event(repo: EventRepo, event_create_factory):
        event_data = event_create_factory.build()
        event_data.total_slots = 10
        event = await repo.create(event_data)
        assert event.id is not None
        assert event.total_slots == 10

async def test_get_by_id(repo: EventRepo, event_create_factory):
        event_data = event_create_factory.build()
        event_data.total_slots = 10
        created = await repo.create(event_data)
        fetched = await repo.get_by_id(created.id)
        assert fetched is not None
        assert fetched.id == created.id

async def test_get_by_id_active(repo: EventRepo, event_create_factory):
        event_data = event_create_factory.build()
        event_data.total_slots = 10
        created = await repo.create(event_data)
        fetched = await repo.get_by_id_active(created.id)
        assert fetched is not None
        assert fetched.id  is not None
        assert fetched.id == created.id

async def test_get_by_id_active_after_delete(repo: EventRepo, event_create_factory):
        event_data = event_create_factory.build()
        event_data.total_slots = 10
        created = await repo.create(event_data)
        await repo.delete(created)
        fetched = await repo.get_by_id_active(created.id)
        assert fetched is None

async def test_update_event(repo: EventRepo, event_create_factory, event_update_factory):
        event_data = event_create_factory.build()
        event_data.total_slots = 10
        created = await repo.create(event_data)
        update_data = event_update_factory.build()
        updated = await repo.update(created, update_data)
        assert updated.id == created.id
        assert updated.updated_at is not None

async def test_delete_event(repo: EventRepo, event_create_factory):
        event_data = event_create_factory.build()
        event_data.total_slots = 10
        created = await repo.create(event_data)
        await repo.delete(created)
        fetched = await repo.get_by_id(created.id)
        assert fetched is not None
        assert fetched.deleted_at is not None

async def test_get_all_stream(repo: EventRepo, event_create_factory):
        for _ in range(3):
            data = event_create_factory.build()
            data.total_slots = 10
            await repo.create(data)
        events = [e async for e in repo.get_all_stream()]
        assert len(events) >= 3

async def test_get_all_pagination(repo: EventRepo, event_create_factory):
        for _ in range(5):
            data = event_create_factory.build()
            data.total_slots = 10
            await repo.create(data)
        page1 = await repo.get_all_pagination(0, 2)
        assert len(page1) == 2

