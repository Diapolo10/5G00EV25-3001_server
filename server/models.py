"""Contains SQLAlchemy database models"""

from sqlalchemy import Column, Float, ForeignKey, Integer, String  # type: ignore

from server.database import Base


class Room:
    """A database model for rooms"""

    __tablename__ = 'rooms'

    room_id = Column(String, primary_key=True, index=True)
