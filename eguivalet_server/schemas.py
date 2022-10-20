"""Contains implementations for Pydantic models used in the API"""

# pylint: disable=missing-class-docstring

import logging
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, SecretStr, validator

from eguivalet_server.config import AccessLevel, MAX_MESSAGE_LENGTH, MIN_MESSAGE_LENGTH

logger = logging.getLogger(__name__)


class HelloWorld(BaseModel):
    """Hello, world!"""

    hello: str


# User models

class UserBase(BaseModel):
    """Base user model"""

    id: UUID = Field(default_factory=uuid4)
    username: str
    email: str  # Consider email validator: https://pydantic-docs.helpmanual.io/usage/types/#pydantic-types


class UserCreate(UserBase):
    """Used when creating a new user"""

    password: SecretStr


class User(UserBase):
    """User of the system"""

    global_access_level: AccessLevel = AccessLevel.BASIC

    class Config:
        orm_mode = True


# Chat models

class Message(BaseModel):
    """Message sent in a chatroom"""

    id: UUID = Field(default_factory=uuid4)
    user_id: UUID
    message: str
    creation_time: datetime = Field(default_factory=datetime.now)

    class Config:
        orm_mode = True

    @validator('message')
    def message_length_acceptable(cls, value):  # pylint: disable=E0213
        """Verify that the message length makes sense"""

        if not MIN_MESSAGE_LENGTH <= len(value):
            raise ValueError("Message is too short")
        if not len(value) <= MAX_MESSAGE_LENGTH:
            raise ValueError("Message is too long")
        return value

    @validator('user_id')
    def user_id_exists(cls, value):  # pylint: disable=E0213
        """Verify that the given user exists (just in case)"""

        return value  # NOTE: Implement if needed


class EncryptedMessage(Message):
    """Encrypted message sent in a chatroom"""


class Room(BaseModel):
    """Chatroom"""

    id: UUID = Field(default_factory=uuid4)
    name: str
    public: bool = True
    owner: Optional[UUID] = None

    class Config:
        orm_mode = True

    @validator('owner')
    def owner_exists(cls, value):  # pylint: disable=E0213
        """Verify that the room owner exists"""

        return value  # NOTE: Add validation

    @validator('owner')
    def public_if_no_owner(cls, value, values):  # pylint: disable=E0213
        """Verify that the server is public if no owner is set"""

        if value is None and values['public'] is False:
            raise ValueError("Private rooms must have an owner")
        return value
