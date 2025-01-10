"""Contains implementations for Pydantic models used in the API."""

from __future__ import annotations

import logging
from datetime import datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, SecretStr, validator

from eguivalet_server.config import MAX_MESSAGE_LENGTH, MIN_MESSAGE_LENGTH, AccessLevel

logger = logging.getLogger(__name__)


class HelloWorld(BaseModel):
    """Hello, world."""

    hello: str


# User models


class UserBase(BaseModel):
    """Base user model."""

    id: UUID = Field(default_factory=uuid4)
    username: str
    email: str  # Consider email validator: https://pydantic-docs.helpmanual.io/usage/types/#pydantic-types


class UserCreate(UserBase):
    """Used when creating a new user."""

    password: SecretStr


class User(UserBase):
    """User of the system."""

    global_access_level: AccessLevel = AccessLevel.BASIC

    class Config:
        """Configure the User schema."""

        orm_mode = True


# Chat models


class Message(BaseModel):
    """Message sent in a chatroom."""

    id: UUID = Field(default_factory=uuid4)
    user_id: UUID
    message: str
    creation_time: datetime = Field(default_factory=datetime.now)

    class Config:
        """Configure the message schema."""

        orm_mode = True

    @validator("message")
    def message_length_acceptable(cls: type[Message], value: str) -> str:  # type: ignore[misc]  # noqa: N805
        """
        Verify that the message length makes sense.

        Raises:
            ValueError: If the given value is not valid.

        Returns:
            The given value if valid.

        """
        if not len(value) >= MIN_MESSAGE_LENGTH:
            msg = "Message is too short"
            raise ValueError(msg)
        if not len(value) <= MAX_MESSAGE_LENGTH:
            msg = "Message is too long"
            raise ValueError(msg)
        return value

    @validator("user_id")
    def user_id_exists(cls: type[Message], value: UUID) -> UUID:  # type: ignore[misc] # noqa: N805
        """
        Verify that the given user exists (just in case).

        Returns:
            The given value (validation pending).

        """
        return value  # NOTE: Implement if needed


class EncryptedMessage(Message):
    """Encrypted message sent in a chatroom."""


class Room(BaseModel):
    """Chatroom."""

    id: UUID = Field(default_factory=uuid4)
    name: str
    public: bool = True
    owner: UUID | None = None

    class Config:
        """Configure the room schema."""

        orm_mode = True

    @validator("owner")
    def owner_exists(cls: type[Room], value: UUID | None) -> UUID | None:  # type: ignore[misc] # noqa: N805
        """
        Verify that the room owner exists.

        Returns:
            The given value (validation pending).

        """
        return value  # NOTE: Add validation

    @validator("owner")
    def public_if_no_owner(cls: type[Room], value: UUID | None, values: dict[str, object]) -> UUID | None:  # type: ignore[misc] # noqa: N805
        """
        Verify that the server is public if no owner is set.

        Raises:
            ValueError: If the room is private and lacks an owner.

        Returns:
            Room UUID if validation was successful.

        """
        if value is None and values["public"] is False:
            msg = "Private rooms must have an owner"
            raise ValueError(msg)
        return value
