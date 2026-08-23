from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict, EmailStr


class BaseBooking(BaseModel):
    user_id: UUID
    event_id: UUID

class BookingCreate(BaseBooking):
    pass

class BookingRead(BaseBooking):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    event_id: UUID
    booking_date: datetime

class BaseEvent(BaseModel):
    title: str
    description: Optional[str] = None
    date: datetime
    total_slots: int
    reserved_slots:int = 0

class EventCreate(BaseEvent):
    pass


class EventUpdate(BaseEvent):
    title:Optional[str] = None 
    description:Optional[str] = None 
    date:Optional[datetime] = None 
    total_slots:Optional[int] = None
    reserved_slots:Optional[int] = None

class EventRead(BaseEvent):
    model_config = ConfigDict(from_attributes=True)

    id: UUID

    reserved_slots: int
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None


