from uuid import UUID

from fastapi import HTTPException, status

from repositories.booking_repo import BookingRepo
from repositories.event_repo import EventRepo
from schemas.event_schema import BookingCreate, EventCreate, EventUpdate


class EventService:

    async def create_event(self, event_data: EventCreate, event_repo: EventRepo):
        try:
            return await event_repo.create(event_data)
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
            )

    async def update_event(
        self, event_id: UUID, event_data: EventUpdate, event_repo: EventRepo
    ):
        try:
            exists_event = await event_repo.get_by_id(event_id)
            if exists_event is None:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                    detail=f"This id {event_id} does not exist",
                )
            return await event_repo.update(exists_event, event_data)
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
            )

    async def delete_event(self, event_id: UUID, event_repo: EventRepo):
        try:
            exists_event = await event_repo.get_by_id(event_id)
            if exists_event is None:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                    detail=f"This id {event_id} does not exist",
                )
            await event_repo.delete(exists_event)
            return {"message": "event deleted successfully"}
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
            )

    async def get_event(self, event_id: UUID, event_repo: EventRepo):
        try:
            exists_event = await event_repo.get_by_id(event_id)
            if exists_event is None:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                    detail=f"This id {event_id} does not exist",
                )
            return exists_event
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
            )

    async def get_list_event(
        self,
        event_repo: EventRepo,
        current_page: int = 1,
        page_size: int = 20,
    ):
        try:
            offset = (current_page - 1) * page_size
            return await event_repo.get_all_pagination(offset, page_size)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
            )

    async def get_slots(self, event_id: UUID, booking_repo: BookingRepo) -> int:
        try:
            return await booking_repo.count_by_event_id(event_id)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
            )

    async def create_booking(
        self,
        event_id: UUID,
        user_id: UUID,
        event_repo: EventRepo,
        booking_repo: BookingRepo,
    ):
        try:
            exists_event = await event_repo.get_by_id(event_id)
            if exists_event is None:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                    detail=f"This id {event_id} does not exist",
                )

            reserved = await booking_repo.count_by_event_id(event_id)
            if reserved >= exists_event.total_slots:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                    detail="No slots available for this event",
                )

            booking_data = BookingCreate(user_id=user_id, event_id=event_id)
            booking = await booking_repo.create(booking_data)

            await event_repo.update(
                exists_event,
                EventUpdate(reserved_slots=reserved + 1),
            )
            return booking
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
            )
