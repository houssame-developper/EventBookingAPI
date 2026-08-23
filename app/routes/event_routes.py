from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query, Request

from api.deps import AdminUser, CurrentUser
from config.limiter import DEFAULT_RATE_LIMIT, limiter
from repositories.booking_repo import BookingRepo
from repositories.event_repo import EventRepo
from schemas.event_schema import BookingRead, EventCreate, EventRead, EventUpdate
from service.event_service import EventService

router = APIRouter(prefix="/events", tags=["events"])
event_service = EventService()


@router.post("", response_model=EventRead)
@limiter.limit(DEFAULT_RATE_LIMIT)
async def create_event(
    request: Request,
    event_data: EventCreate,
    _: AdminUser,
    event_repo: Annotated[EventRepo, Depends()],
):
    event = await event_service.create_event(event_data, event_repo)
    return EventRead.model_validate(event, from_attributes=True)


@router.get("", response_model=list[EventRead])
@limiter.limit(DEFAULT_RATE_LIMIT)
async def list_events(
    request: Request,
    event_repo: Annotated[EventRepo, Depends()],
    current_page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
):
    events = await event_service.get_list_event(event_repo, current_page, page_size)
    return [EventRead.model_validate(e, from_attributes=True) for e in events]


@router.get("/{event_id}", response_model=EventRead)
@limiter.limit(DEFAULT_RATE_LIMIT)
async def get_event(
    request: Request,
    event_id: UUID,
    event_repo: Annotated[EventRepo, Depends()],
):
    event = await event_service.get_event(event_id, event_repo)
    return EventRead.model_validate(event, from_attributes=True)


@router.patch("/{event_id}", response_model=EventRead)
@limiter.limit(DEFAULT_RATE_LIMIT)
async def update_event(
    request: Request,
    event_id: UUID,
    event_data: EventUpdate,
    _: AdminUser,
    event_repo: Annotated[EventRepo, Depends()],
):
    event = await event_service.update_event(event_id, event_data, event_repo)
    return EventRead.model_validate(event, from_attributes=True)


@router.delete("/{event_id}")
@limiter.limit(DEFAULT_RATE_LIMIT)
async def delete_event(
    request: Request,
    event_id: UUID,
    _: AdminUser,
    event_repo: Annotated[EventRepo, Depends()],
):
    return await event_service.delete_event(event_id, event_repo)


@router.get("/{event_id}/slots")
@limiter.limit(DEFAULT_RATE_LIMIT)
async def get_event_slots(
    request: Request,
    event_id: UUID,
    booking_repo: Annotated[BookingRepo, Depends()],
):
    reserved = await event_service.get_slots(event_id, booking_repo)
    return {"event_id": event_id, "reserved_slots": reserved}


@router.post("/{event_id}/bookings", response_model=BookingRead)
@limiter.limit(DEFAULT_RATE_LIMIT)
async def create_booking(
    request: Request,
    event_id: UUID,
    current_user: CurrentUser,
    event_repo: Annotated[EventRepo, Depends()],
    booking_repo: Annotated[BookingRepo, Depends()],
):
    booking = await event_service.create_booking(
        event_id, current_user.id, event_repo, booking_repo
    )
    return BookingRead.model_validate(booking, from_attributes=True)
