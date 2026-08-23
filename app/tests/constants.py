import pytest
from polyfactory.factories.pydantic_factory import ModelFactory
from schemas.user_schema import UserCreate, UserRead, UserUpdate, Register, Login
from schemas.event_schema import EventCreate, EventRead, EventUpdate, BookingCreate, BookingRead
from unittest.mock import Mock
from fastapi import Response


@pytest.fixture(scope="function")
def response_mock() -> Mock:
    return Mock(spec=Response)


class TestUserCreateFactory(ModelFactory[UserCreate]):
    __model__ = UserCreate

class TestUserReadFactory(ModelFactory[UserRead]):
    __model__ = UserRead

class TestUserUpdateFactory(ModelFactory[UserUpdate]):
    __model__ = UserUpdate

class TestRegisterFactory(ModelFactory[Register]):
    __model__ = Register

class TestLoginFactory(ModelFactory[Login]):
    __model__ = Login 

class TestEventCreateFactory(ModelFactory[EventCreate]):
    __model__ = EventCreate

class TestEventReadFactory(ModelFactory[EventRead]):
    __model__ = EventRead

class TestEventUpdateFactory(ModelFactory[EventUpdate]):
    __model__ = EventUpdate

class TestBookingCreateFactory(ModelFactory[BookingCreate]):
    __model__ = BookingCreate

class TestBookingReadFactory(ModelFactory[BookingRead]):
    __model__ = BookingRead


@pytest.fixture
def user_create_factory() -> type[TestUserCreateFactory]:
    return TestUserCreateFactory

@pytest.fixture
def user_read_factory() -> type[TestUserReadFactory]:
    return TestUserReadFactory

@pytest.fixture
def user_update_factory() -> type[TestUserUpdateFactory]:
    return TestUserUpdateFactory

@pytest.fixture
def register_factory() -> type[TestRegisterFactory]:
    return TestRegisterFactory

@pytest.fixture
def login_factory() -> type[TestLoginFactory]:
    return TestLoginFactory

@pytest.fixture
def event_create_factory() -> type[TestEventCreateFactory]:
    return TestEventCreateFactory

@pytest.fixture
def event_read_factory() -> type[TestEventReadFactory]:
    return TestEventReadFactory

@pytest.fixture
def event_update_factory() -> type[TestEventUpdateFactory]:
    return TestEventUpdateFactory

@pytest.fixture
def booking_create_factory() -> type[TestBookingCreateFactory]:
    return TestBookingCreateFactory

@pytest.fixture
def booking_read_factory() -> type[TestBookingReadFactory]:
    return TestBookingReadFactory