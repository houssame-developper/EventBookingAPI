from typing import Annotated

from fastapi import APIRouter, Depends, Request

from api.deps import CurrentUser
from config.limiter import DEFAULT_RATE_LIMIT, limiter
from repositories.booking_repo import BookingRepo
from schemas.event_schema import BookingRead

router = APIRouter(prefix="/bookings", tags=["bookings"])


@router.get("/me", response_model=list[BookingRead])
@limiter.limit(DEFAULT_RATE_LIMIT)
async def my_bookings(
    request: Request,
    current_user: CurrentUser,
    booking_repo: Annotated[BookingRepo, Depends()],
):
    bookings = await booking_repo.get_by_user_id(current_user.id)
    return [BookingRead.model_validate(b, from_attributes=True) for b in bookings]
