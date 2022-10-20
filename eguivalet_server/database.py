"""Contains functionality needed to get a database session"""

from sqlalchemy import create_engine  # type: ignore
from sqlalchemy.ext.declarative import declarative_base  # type: ignore
from sqlalchemy.orm import sessionmaker  # type: ignore

from eguivalet_server.config import (
    SQLALCHEMY_DATABASE_URL,
)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={
        'check_same_thread': False,
    }
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """Yields and auto-closes a database session"""

    db_session = SessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()
