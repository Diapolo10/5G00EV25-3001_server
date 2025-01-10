"""Contains functionality needed to get a database session."""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

from eguivalet_server.config import (
    SQLALCHEMY_DATABASE_URL,
)

if TYPE_CHECKING:
    from collections.abc import Generator

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={
        "check_same_thread": False,
    },
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """
    Yield and auto-close a database session.

    Yields:
        A database session.

    """
    db_session = SessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()
