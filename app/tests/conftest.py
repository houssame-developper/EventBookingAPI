import os
from typing import AsyncGenerator
import pytest
import pytest_asyncio
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from httpx import AsyncClient, ASGITransport

from main import app
from config.database import get_db

TEST_DATABASE_URL = os.environ.get("TEST_DATABASE_URL")

if not TEST_DATABASE_URL:
    raise ValueError("TEST_DATABASE_URL environment variable is not set.")

# 1. إنشاء Engine واحد فقط على مستوى الـ Session ليعمل مع نفس الـ Event Loop
@pytest_asyncio.fixture(scope="session")
def test_engine():
    engine = create_async_engine(
        TEST_DATABASE_URL,
        echo=False,  # إيقاف طباعة الاستعلامات للحد من استهلاك الـ I/O
        future=True
    )
    yield engine
    # يتم إغلاقه عند انتهاء كل الاختبارات
    engine.sync_engine.dispose()

# 2. إنشاء الجداول مرة واحدة فقط في بداية تشغيل Pytest ومسحها عند الانتهاء كلياً
@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_test_db(test_engine):
    async with test_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)

# 3. إدارة الـ Sessions بأسلوب الـ Rollback السريع جدًا لكل اختبار
@pytest_asyncio.fixture(scope="function")
async def db_session(test_engine) -> AsyncGenerator[AsyncSession, None]:
    # فتح Connection فردي لكل test
    async with test_engine.connect() as connection:
        # بدء Transaction
        transaction = await connection.begin()
        
        # إنشاء Session مرتبطة بهذا الـ Connection المباشر
        async_session = AsyncSession(
            bind=connection,
            expire_on_commit=False,
            join_transaction_mode="create_savepoint"  # يمنع الـ Commit الحقيقي داخل الكود
        )

        yield async_session

        # التنظيف السريع في الميلي ثواني: إغلاق الجلسة وإلغاء التغييرات فوراً
        await async_session.close()
        await transaction.rollback()

# 4. ربط FastAPI بنفس الـ Session الخاصة بالاختبار لمنع تضارب الجلسات
@pytest_asyncio.fixture(scope="function")
async def client(db_session: AsyncSession):
    async def _override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = _override_get_db
    
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://testserver"
    ) as c:
        yield c
        
    app.dependency_overrides.clear()
