"""Contains implementations for Pydantic models used in the API"""

# pylint: disable=missing-class-docstring

from __future__ import annotations
import logging
from datetime import datetime
from typing import Any
from uuid import UUID, uuid4

from fastapi_users import schemas as user_schemas
from pydantic import BaseModel, Field, SecretStr, validator

from eguivalet_server.config import MAX_MESSAGE_LENGTH, MIN_MESSAGE_LENGTH, AccessLevel

logger = logging.getLogger(__name__)


class HelloWorld(BaseModel):
    """Hello, world!"""

    hello: str


# User models

class UserRead(user_schemas.BaseUser[UUID]):
    """User read data"""

    # id: UUID = Field(default_factory=uuid4)
    username: str
    # email: str  # Consider email validator: https://pydantic-docs.helpmanual.io/usage/types/#pydantic-types


class UserCreate(user_schemas.BaseUserCreate):
    """User write data"""

    username: str
    global_access_level: AccessLevel = AccessLevel.BASIC


class UserUpdate(user_schemas.BaseUserUpdate):
    """User update data"""

    username: str
    global_access_level: AccessLevel | None = None


# Chat models

class Message(BaseModel):
    """Message sent in a chatroom"""

    id: UUID = Field(default_factory=uuid4)  # noqa: A003
    user_id: UUID
    message: str
    creation_time: datetime = Field(default_factory=datetime.now)

    class Config:
        orm_mode = True

    @validator('message')
    def message_length_acceptable(cls: Message, value: str) -> str:  # noqa: N805
        """Verify that the message length makes sense"""

        if not len(value) >= MIN_MESSAGE_LENGTH:
            raise ValueError("Message is too short")
        if not len(value) <= MAX_MESSAGE_LENGTH:
            raise ValueError("Message is too long")
        return value

    @validator('user_id')
    def user_id_exists(cls: Message, value: UUID) -> UUID:  # noqa: N805
        """Verify that the given user exists (just in case)"""

        return value  # NOTE: Implement if needed


class EncryptedMessage(Message):
    """Encrypted message sent in a chatroom"""


class Room(BaseModel):
    """Chatroom"""

    id: UUID = Field(default_factory=uuid4)  # noqa: A003
    name: str
    public: bool = True
    owner: UUID | None = None

    class Config:
        orm_mode = True

    @validator('owner')
    def owner_exists(cls: Room, value: UUID | None) -> UUID | None:  # noqa: N805
        """Verify that the room owner exists"""

        return value  # NOTE: Add validation

    @validator('owner')
    def public_if_no_owner(cls: Room, value: UUID | None, values: dict[str, Any]) -> UUID | None:  # noqa: N805
        """Verify that the server is public if no owner is set"""

        if value is None and values['public'] is False:
            raise ValueError("Private rooms must have an owner")
        return value
