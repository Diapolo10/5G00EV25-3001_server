"""Unit test configurations."""

# pylint: disable=W0621

import uuid
from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from pydantic import SecretStr
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy_utils import create_database, database_exists

from eguivalet_server import crud, schemas
from eguivalet_server.config import (
    SQLALCHEMY_TEST_DATABASE_URL,
)
from eguivalet_server.database import Base, get_db
from eguivalet_server.main import app


@pytest.fixture(scope='session')
def db_engine():
    """Create a test database and yields a database engine."""
    engine = create_engine(
        SQLALCHEMY_TEST_DATABASE_URL,
        connect_args={
            'check_same_thread': False,
        },
    )

    if not database_exists:  # type: ignore[truthy-function]
        create_database(engine.url)

    Base.metadata.create_all(bind=engine)
    return engine


@pytest.fixture
def db_session(db_engine):
    """Create a connection to the test database and handles cleanup."""
    connection = db_engine.connect()

    # Begin a non-ORM transaction
    _ = connection.begin()

    database_session = Session(bind=connection, expire_on_commit=False)

    yield database_session

    database_session.rollback()
    connection.close()


@pytest.fixture
def client(db_session) -> Generator[TestClient, None, None]:
    """
    Override the normal database access with test database.

    Yields a configured test client.
    """
    app.dependency_overrides[get_db] = lambda: db_session

    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def public_rooms(db_session) -> list[uuid.UUID]:
    """Add some example public rooms to the database."""
    rooms: list[uuid.UUID] = [
        crud.create_room(
            db_session,
            schemas.Room(name=f"Public Room #{num}", public=True),
        ).id
        for num in range(5)
    ]

    return rooms


@pytest.fixture
def test_users(db_session) -> list[uuid.UUID]:
    """Add some example users to the database."""
    # NOTE: Maybe randomise in the future
    users: list[uuid.UUID] = [
        crud.create_user(
            db_session,
            schemas.UserCreate(
                username=f"TestUser{num}",
                email=f"test.user{num}@jmail.com",
                password=SecretStr("CORRECT HORSE BATTERY STAPLE"),
            ),
        ).id
        for num in range(5)
    ]

    return users


@pytest.fixture
def private_rooms(db_session, test_users) -> list[uuid.UUID]:
    """Add some example private rooms to the database."""
    rooms: list[uuid.UUID] = [
        crud.create_room(
            db_session,
            schemas.Room(
                name=f"Private Room #{num}",
                public=False,
                owner=user,
            ),
        ).id
        for num, user in enumerate(test_users)
    ]

    return rooms
