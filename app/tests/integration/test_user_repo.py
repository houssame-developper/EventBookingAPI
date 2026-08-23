import pytest
from models import User, UserRole
from repositories.user_repo import UserRepo
from tests.constants import user_create_factory, user_update_factory
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.fixture(scope="function")
def repo(db_session: AsyncSession):
    return UserRepo(db_session)

async def test_create_user(repo: UserRepo, user_create_factory):
        user_data = user_create_factory.build()
        user = await repo.create(user_data)
        assert user.id is not None
        assert user.email == user_data.email
        assert user.password_hash != user_data.password

async def test_get_by_id(repo: UserRepo, user_create_factory):
        user_data = user_create_factory.build()
        created = await repo.create(user_data)
        fetched = await repo.get_by_id(created.id)
        assert fetched is not None
        assert fetched.id == created.id
        assert fetched.email == user_data.email

async def test_get_by_email(repo: UserRepo, user_create_factory):
        user_data = user_create_factory.build()
        await repo.create(user_data)
        fetched = await repo.get_by_email(user_data.email)
        assert fetched is not None
        assert fetched.email == user_data.email

async def test_update_user(repo: UserRepo, user_create_factory, user_update_factory):
        user_data = user_create_factory.build()
        created = await repo.create(user_data)
        update_data = user_update_factory.build()
        updated = await repo.update(created, update_data)
        assert updated.id == created.id
        assert updated.updated_at is not None

async def test_delete_user(repo: UserRepo, user_create_factory):
        user_data = user_create_factory.build()
        created = await repo.create(user_data)
        await repo.delete(created)
        fetched = await repo.get_by_id(created.id)
        assert fetched is not None
        assert fetched.deleted_at is not None

async def test_get_all_stream(repo: UserRepo, user_create_factory):
        await repo.create(user_create_factory.build())
        await repo.create(user_create_factory.build())
        users = [u async for u in repo.get_all_stream()]
        assert len(users) >= 2

async def test_get_all_pagination(repo: UserRepo, user_create_factory):
        for _ in range(5):
            await repo.create(user_create_factory.build())
        page1 = await repo.get_all_pagination(0, 2)
        assert len(page1) == 2
        page2 = await repo.get_all_pagination(2, 2)
        assert len(page2) == 2