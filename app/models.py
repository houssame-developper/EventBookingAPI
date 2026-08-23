from datetime import datetime, timezone
from enum import Enum as PyEnum 
from uuid import uuid7, UUID
from typing import List, Optional
from pydantic import EmailStr
from sqlmodel import SQLModel, Field, Relationship, text,DateTime
from sqlalchemy import Column, Enum as SqlEnum, True_
import sqlalchemy as sa

class UserRole(str, PyEnum):
    ADMIN = "admin"
    USER = "user"

class Booking(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid7, primary_key=True, index=True)
    user_id: UUID = Field(foreign_key="user.id", index=True,ondelete="RESTRICT") 
    event_id: UUID = Field(foreign_key="event.id", index=True,ondelete="RESTRICT") 
    booking_date: Optional[datetime]  = Field(sa_type=DateTime(timezone=True),sa_column_kwargs={"server_default": text("current_timestamp")},
                                   default=None)

class User(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid7, primary_key=True, index=True)
    name: str = Field(min_length=3, max_length=200) 
    email: EmailStr = Field(min_length=3, max_length=255, unique=True)
    password_hash: str = Field(max_length=255)
    
    role:UserRole = Field(
        sa_column=Column(SqlEnum(UserRole), default=UserRole.USER, nullable=False)
    )

    created_at: Optional[datetime]  = Field(
        sa_type=DateTime(timezone=True),
        sa_column_kwargs={"server_default": text("current_timestamp")},
        default=None
    )    
    updated_at: Optional[datetime]  = Field(
        sa_type=DateTime(timezone=True),
        sa_column_kwargs={"server_default": text("current_timestamp"),
                          "onupdate": text("current_timestamp")},
                          default=None
    )    
    deleted_at: Optional[datetime] = Field(
            default=None,
            sa_type=DateTime(timezone=True),
            nullable=True
        )

    events: List["Event"] = Relationship(back_populates="users", link_model=Booking)
    

class Event(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid7, primary_key=True, index=True)
    title: str = Field(min_length=3, max_length=200)
    description: Optional[str] = Field(default=None, min_length=20, max_length=500) 
    date: Optional[datetime] = Field(sa_type=DateTime(timezone=True),default_factory=lambda: datetime.now(timezone.utc))
    total_slots: int = Field(sa_column=sa.Column(
            sa.Integer, 
            sa.CheckConstraint('total_slots >= 1', name='ck_event_total_slots_min'),
            nullable=False
        ),default=1)

    reserved_slots:int = Field( sa_column=sa.Column(
            sa.Integer, 
            sa.CheckConstraint('reserved_slots >= 0', name='ck_event_reserved_slots_min'),
            nullable=False
        ),default=0)  

    created_at: datetime = Field( 
        sa_type=DateTime(timezone=True),
        sa_column_kwargs={"server_default": text("current_timestamp")},
        default=None
    )    
    updated_at: datetime = Field(
        sa_type=DateTime(timezone=True),
        sa_column_kwargs={"server_default": text("current_timestamp"),
                          "onupdate": text("current_timestamp")},
                          default=None)

    
    deleted_at: Optional[datetime] = Field(
            default=None,
            sa_type=DateTime(timezone=True),
            nullable=True
        )
    users: List["User"] = Relationship(back_populates="events", link_model=Booking)
