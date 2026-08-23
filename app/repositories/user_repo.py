from fastapi import Depends
from fastapi.concurrency import run_in_threadpool
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from config.auth_utils import hashing_password, verify_password
from config.database import get_db
from models import User, UserRole
from schemas.user_schema import BaseUser, Register, UserCreate, UserUpdate
from repositories.base_repo import BaseRepo


class UserRepo(BaseRepo[User,BaseUser]):
    def __init__(self, session: AsyncSession = Depends(get_db)):
        super().__init__(session, User)

    def process_before(self, password: str) -> str:
        return hashing_password(password)

    def process_after(self, password: str, hash_password: str) -> bool:
        return verify_password(password, hash_password=hash_password)

    async def create(self, item_data: UserCreate | Register) -> User:
        password_hash = await run_in_threadpool(self.process_before,item_data.password)
        user = User(
            name=item_data.name,
            email=item_data.email,
            password_hash=password_hash,
            role=item_data.role if hasattr(item_data,"role") else None,
        )
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def update(self, item: User, item_data: UserUpdate) -> User:
        from datetime import datetime, timezone
        update_data = item_data.model_dump(exclude_unset=True,exclude_none=True)
        for field,value in update_data.items():
            if field == "password":
                if item_data.password:
                    item.password_hash = await run_in_threadpool(self.process_before,value)
                continue
            setattr(item, field, value)
        item.updated_at = datetime.now(timezone.utc)
        self.session.add(item)
        await self.session.commit()
        await self.session.refresh(item)
        return item


    async def get_by_email(self, email: str) -> User | None:
        stmt = select(User).where(User.email == email)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()