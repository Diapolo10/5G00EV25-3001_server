"""Contains SQLAlchemy database models"""

from sqlalchemy import Column, String  # type: ignore

from server.database import Base


class Room(Base):
    """A database model for rooms"""

    __tablename__ = 'rooms'

    room_id = Column(String, primary_key=True, index=True)
