"""Unit test configurations"""

# pylint: disable=W0621

import uuid
from typing import List

import pytest
from fastapi.testclient import TestClient
from pydantic import SecretStr
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy_utils import database_exists, create_database

from server.config import (
    SQLALCHEMY_TEST_DATABASE_URL,
)
from server.database import Base, get_db
from server.main import app
from server import crud, schemas


@pytest.fixture(scope='session')
def db_engine():
    """Creates a test database and yields a database engine"""

    engine = create_engine(
        SQLALCHEMY_TEST_DATABASE_URL,
        connect_args={
            'check_same_thread': False
        }
    )

    if not database_exists:
        create_database(engine.url)

    Base.metadata.create_all(bind=engine)
    yield engine


@pytest.fixture(scope='function')
def db_session(db_engine):
    """Creates a connection to the test database and handles cleanup"""

    connection = db_engine.connect()

    # Begin a non-ORM transaction
    _ = connection.begin()

    database_session = Session(bind=connection, expire_on_commit=False)

    yield database_session

    database_session.rollback()
    connection.close()


@pytest.fixture(scope='function')
def client(db_session):
    """
    Overrides the normal database access with test database,
    and yields a configured test client
    """

    app.dependency_overrides[get_db] = lambda: db_session

    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def public_rooms(db_session):
    """
    Adds some example public rooms to the database
    """

    rooms: List[uuid.UUID] = [
        crud.create_room(
            db_session,
            schemas.Room(name=f"Public Room #{num}", public=True)
        ).id
        for num in range(5)
    ]

    yield rooms


@pytest.fixture
def test_users(db_session):
    """
    Adds some example users to the database
    """

    # NOTE: Maybe randomise in the future
    users: List[uuid.UUID] = [
        crud.create_user(
            db_session,
            schemas.UserCreate(
                username=f"TestUser{num}",
                email=f"test.user{num}@jmail.com",
                password=SecretStr("CORRECT HORSE BATTERY STAPLE")
            )
        ).id
        for num in range(5)
    ]

    yield users


@pytest.fixture
def private_rooms(db_session, test_users):
    """
    Adds some example private rooms to the database
    """

    rooms: List[uuid.UUID] = [
        crud.create_room(
            db_session,
            schemas.Room(
                name=f"Private Room #{num}",
                public=False,
                owner=user
            )
        ).id
        for num, user in enumerate(test_users)
    ]

    yield rooms
