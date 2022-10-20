"""Contains SQLAlchemy database models"""

import uuid

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship
from sqlalchemy_utils import UUIDType  # type: ignore

from eguivalet_server.config import (
    AccessLevel,
    MAX_EMAIL_ADDRESS_LENGTH,
    MAX_MESSAGE_LENGTH,
    MAX_PASSWORD_HASH_LENGTH,
    MAX_USERNAME_LENGTH,
)
from eguivalet_server.database import Base


# Link tables


users_in_rooms_table = Table(
    'users_in_rooms',
    Base.metadata,
    Column('user_id', ForeignKey('users.id'), primary_key=True),
    Column('room_id', ForeignKey('rooms.id'), primary_key=True)
)


# Others


class Room(Base):
    """A database model for rooms"""

    __tablename__ = 'rooms'

    id = Column(UUIDType(binary=False), primary_key=True, index=True, default=uuid.uuid4)
    name = Column(String(MAX_MESSAGE_LENGTH))
    public = Column(Boolean, default=True)
    owner = Column(UUIDType(binary=False), nullable=True, default=None)

    messages = relationship("Message", back_populates='room')
    users = relationship("User", secondary=users_in_rooms_table, backref='chatrooms')


class Message(Base):
    """A database model for messages"""

    __tablename__ = 'messages'

    id = Column(UUIDType(binary=False), primary_key=True, index=True, default=uuid.uuid4)
    user_id: Column[uuid.UUID] = Column(ForeignKey('users.id'))  # type: ignore
    room_id: Column[uuid.UUID] = Column(ForeignKey('rooms.id'))  # type: ignore
    message = Column(String(MAX_MESSAGE_LENGTH))
    creation_time = Column(DateTime)
    last_edited = Column(DateTime, nullable=True, default=None)

    room = relationship("Room", back_populates='messages')


class User(Base):
    """A database model for users"""

    __tablename__ = 'users'

    id = Column(UUIDType(binary=False), primary_key=True, index=True, default=uuid.uuid4, nullable=False)
    username = Column(String(MAX_USERNAME_LENGTH))
    email = Column(String(MAX_EMAIL_ADDRESS_LENGTH), unique=True)
    password_hash = Column(String(MAX_PASSWORD_HASH_LENGTH))
    global_access_level = Column(Integer, default=AccessLevel.BASIC)
