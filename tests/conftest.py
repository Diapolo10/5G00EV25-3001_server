"""Unit test configurations"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine  # type: ignore
from sqlalchemy.core import Session  # type: ignore
from sqlalchemy_utils import database_exists, create_database  # type: ignore

from server.config import (
    SQLALCHEMY_TEST_DATABASE_URL,
)
from server.database import Base, get_db
from server.main import app


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
def db(db_engine):
    """Creates a connection to the test database and handles cleanup"""

    connection = db_engine.connect()

    # Begin a non-ORM transaction
    _ = connection.begin()

    db = Session(bind=connection, expire_on_commit=False)

    yield db

    db.rollback()
    connection.close()


@pytest.fixture(scope='function')
def client(db):
    """
    Overrides the normal database access with test database,
    and yields a configured test client
    """

    app.dependency_overrides[get_db] = lambda: db

    with TestClient(app) as c:
        yield c


# @pytest.fixture
# def filled_database(db):
#     populate_database(db)
