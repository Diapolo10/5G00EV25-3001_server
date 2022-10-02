"""Contains implementations for Pydantic models used in the API"""

# pylint: disable=missing-class-docstring

import logging
from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, SecretStr, validator

from server.config import MAX_MESSAGE_LENGTH, MIN_MESSAGE_LENGTH

logger = logging.getLogger(__name__)


class HelloWorld(BaseModel):
    """Hello, world!"""

    hello: str


# Enums

class AccessLevel(Enum):
    'banned'
    'basic'
    'verified'
    'moderator'
    'administrator'


# User models

class UserBase(BaseModel):
    """Base user model"""

    id: UUID
    username: str
    email: str  # Consider email validator in the future: https://pydantic-docs.helpmanual.io/usage/types/#pydantic-types


class UserCreate(UserBase):
    """Used when creating a new user"""

    password: SecretStr


class User(UserBase):
    """User of the system"""

    global_access_level: AccessLevel

    class Config:
        orm_mode = True


# Chat models

class Message(BaseModel):
    """Message sent in a chatroom"""

    id: UUID
    user_id: UUID
    message: str
    timestamp: datetime

    class Config:
        orm_mode = True

    @validator('message')
    def message_length_acceptable(cls, value):
        """Verify that the message length makes sense"""

        if not MIN_MESSAGE_LENGTH <= len(value):
            raise ValueError("Message is too short")
        elif not len(value) <= MAX_MESSAGE_LENGTH:
            raise ValueError("Message is too long")
        return value

    @validator('user_id')
    def user_id_exists(cls, value):
        """Verify that the given user exists (just in case)"""

        return value  # NOTE: Implement if needed


class EncryptedMessage(Message):
    """Encrypted message sent in a chatroom"""


class Room(BaseModel):
    """Chatroom"""

    id: UUID
    name: str
    public: bool
    owner: UUID | None

    class Config:
        orm_mode = True

    @validator('owner')
    def owner_exists(cls, value):
        return value  # NOTE: Add validation
    
    @validator('owner')
    def public_if_no_owner(cls, value, values, **kwargs):
        if value is None and values['public'] == False:
            raise ValueError("Private rooms must have an owner")
        return value

