from uuid import UUID

try:
    from app.schemas.event_schema import BaseEvent
except ModuleNotFoundError:
    from schemas.event_schema import BaseEvent
from fastapi import Depends
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from config.database import get_db
from models import Event
from repositories.base_repo import BaseRepo


class EventRepo(BaseRepo[Event,BaseEvent]):
    def __init__(self, session: AsyncSession = Depends(get_db)):
        super().__init__(session, Event)

    async def get_by_id_active(self, event_id: UUID) -> Event | None:
        stmt = select(Event).where(Event.id == event_id, Event.deleted_at.is_(None))
        result = await  self.session.execute(stmt)
        return result.scalar_one_or_none()