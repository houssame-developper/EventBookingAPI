from dotenv import load_dotenv
import pytest
import os
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import NullPool
from sqlmodel import SQLModel
from main import app
from httpx import AsyncClient, ASGITransport
from config.database import get_db

TEST_DATABASE_URL = os.environ.get("TEST_DATABASE_URL")

if not TEST_DATABASE_URL:
    raise ValueError("TEST_DATABASE_URL environment variable is not set in .env.test file.")

@pytest.fixture(scope="function")
async def setup_test_db():
    """Fixture to set up the test database."""
    test_engine = create_async_engine(TEST_DATABASE_URL, echo=True, future=True, poolclass=NullPool)
    
    async with test_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    
    yield test_engine
    
    async with test_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
    
    await test_engine.dispose()


@pytest.fixture(scope="function")
async def db_session(setup_test_db) -> AsyncGenerator[AsyncSession, None]:
    """Fixture to provide an async session for tests."""
    test_engine = setup_test_db
    async_session = async_sessionmaker(test_engine, class_=AsyncSession, expire_on_commit=False)
    session = async_session()
    try:
        yield session
    except Exception as e:
        await session.rollback()
        raise e
    finally:
        await session.close()


@pytest.fixture(scope="function")
async def client(db_session: AsyncSession):
    async def _override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = _override_get_db
    async with AsyncClient(transport=ASGITransport(app=app),base_url="http://testserver") as c:
        yield c
    app.dependency_overrides.clear()