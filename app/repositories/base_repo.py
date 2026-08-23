from abc import ABC
from datetime import datetime, timezone
from typing import Type, TypeVar, Sequence, Any, Generic
from uuid import UUID

from pydantic import BaseModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import SQLModel, select

T = TypeVar("T", bound=SQLModel)
A = TypeVar("A", bound=BaseModel)

class BaseRepo(ABC, Generic[T, A]):
    __slots__ = ["session", "model"] 

    def __init__(self, session: AsyncSession, model: Type[T]):
        self.session: AsyncSession = session
        self.model: Type[T] = model 

    async def create(self, item_data: A) -> T:
        item = self.model.model_validate(item_data)
        self.session.add(item)
        await self.session.commit()
        await self.session.refresh(item) 
        return item

    async def update(self, item: T, item_data: A) -> T:

        update_data = item_data.model_dump(exclude_unset=True, exclude_none=True)

        for field, value in update_data.items():
            setattr(item, field, value)

        item.updated_at = datetime.now(timezone.utc)
        self.session.add(item)
        await self.session.commit()
        await self.session.refresh(item)
        return item

    async def delete(self, item: T) -> None:
        item.deleted_at = datetime.now(timezone.utc) 
        self.session.add(item)  
        await self.session.commit()

    async def get_by_id(self, item_id: Any) -> T | None:
        return await self.session.get(self.model, item_id)


    async def get_all_stream(self):
        result = await self.session.execute(select(self.model))
        for item in result:
            yield item    

    async def get_all_pagination(self, calculated_offset: int, page_size: int) -> Sequence[T]:
        stmt = select(self.model).offset(calculated_offset).limit(page_size)
        result = await self.session.execute(stmt)
        return result.scalars().all()  
            
    async def process_before(self, item: T) -> None:
        pass

    async def process_after(self, item: T) -> None:
        pass