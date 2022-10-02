"""Contains SQLAlchemy database models"""

import uuid

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship
from sqlalchemy_utils import UUIDType

from server.config import (
    MAX_EMAIL_ADDRESS_LENGTH,
    MAX_MESSAGE_LENGTH,
    MAX_PASSWORD_HASH_LENGTH,
    MAX_USERNAME_LENGTH,
)
from server.database import Base


# Link tables


users_in_rooms_table = Table(
    "users_in_rooms",
    Base.metadata,
    Column("left_id", ForeignKey("left.id"), primary_key=True),
    Column("right_id", ForeignKey("right.id"), primary_key=True)
)


# Others


class Room(Base):
    """A database model for rooms"""

    __tablename__ = 'rooms'

    id = Column(UUIDType(binary=False), primary_key=True, index=True, default=uuid.uuid4)
    name = Column(String(MAX_MESSAGE_LENGTH))
    public = Column(Boolean, default=True)
    owner = Column(UUIDType(binary=False), nullable=True, default=None)

    messages = relationship("Message", back_populates="room")
    users = relationship("User", secondary=users_in_rooms_table, backref="chatrooms")


class Message(Base):
    """A database model for messages"""

    __tablename__ = 'messages'

    id = Column(UUIDType(binary=False), primary_key=True, index=True, default=uuid.uuid4)
    user_id = Column(UUIDType(binary=False), default=uuid.uuid4)
    message = Column(String(MAX_MESSAGE_LENGTH))
    timestamp = Column(DateTime)

    room = relationship("Room", back_populates="messages")


class User(Base):
    """A database model for users"""

    __tablename__ = 'users'

    id = Column(UUIDType(binary=False), primary_key=True, index=True, default=uuid.uuid4)
    username = Column(String(MAX_USERNAME_LENGTH))
    email = Column(String(MAX_EMAIL_ADDRESS_LENGTH), unique=True)
    password_hash = Column(String(MAX_PASSWORD_HASH_LENGTH))
    global_access_level = Column(Integer, default=1)
