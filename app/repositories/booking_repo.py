from typing import Sequence
from uuid import UUID

try:
    from app.schemas.event_schema import BaseBooking
except ModuleNotFoundError:
    from schemas.event_schema import BaseBooking
from fastapi import Depends
from sqlmodel import func, select
from sqlmodel.ext.asyncio.session import AsyncSession

from config.database import get_db
from models import Booking
from repositories.base_repo import BaseRepo


class BookingRepo(BaseRepo[Booking,BaseBooking]):
    def __init__(self, session: AsyncSession = Depends(get_db)):
        super().__init__(session, Booking)

    async def count_by_event_id(self, event_id: UUID) -> int:
        stmt = (
            select(func.count())
            .select_from(Booking)
            .where(Booking.event_id == event_id)
        )
        result = await self.session.execute(stmt)
        return result.scalar()

    async def get_by_user_id(self, user_id: UUID) -> Sequence[Booking]:
        stmt = select(Booking).where(Booking.user_id == user_id)
        result = await self.session.execute(stmt)
        return result.scalars().all()

