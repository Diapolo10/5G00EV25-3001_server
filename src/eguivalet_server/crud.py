"""C.R.U.D. - Create Read Update Delete."""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import TYPE_CHECKING

from eguivalet_server import models, schemas

if TYPE_CHECKING:
    from uuid import UUID

    from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)


def read_public_rooms(db: Session) -> list[models.Room]:
    """
    Fetch all public rooms.

    Returns:
        A list of room database models.

    """
    return (
        db.query(models.Room)
        .filter(models.Room.public is True)
        .all()
    )


def read_room(db: Session, room_id: UUID) -> models.Room | None:
    """
    Fetch a room by the room ID.

    Returns:
        The room model, or None if not found.

    """
    return db.query(models.Room).filter(models.Room.id == room_id).first()


def create_room(db: Session, room: schemas.Room) -> models.Room:
    """
    Create a new room.

    Returns:
        A new room model.

    """
    db_room = models.Room(**room.dict())
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    return db_room


def delete_room(db: Session, room_id: UUID) -> None:
    """Delete an existing room."""
    db.query(models.Room).filter(models.Room.id == room_id).delete()
    db.commit()


def read_user(db: Session, user_id: UUID) -> models.User | None:
    """
    Get a user by the user ID.

    Returns:
        User model, or None if not found.

    """
    return db.query(models.User).filter(models.User.id == user_id).first()


def read_user_by_email(db: Session, email: str) -> models.User | None:
    """
    Get a user by the user email.

    Returns:
        User model, or None if not found.

    """
    return db.query(models.User).filter(models.User.email == email).first()


def read_users(db: Session, skip: int = 0, limit: int | None = None) -> list[models.User]:
    """
    Get all users.

    Returns:
        A list of user models.

    """
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    """
    Create a new user.

    Returns:
        Newly created user model.

    """
    fake_hashed_password = user.password.get_secret_value() + "generate_salt_here_and_hash"
    db_user = models.User(
        email=user.email,
        username=user.username,
        password_hash=fake_hashed_password,
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def read_message(db: Session, room_id: UUID, message_id: UUID) -> models.Message | None:
    """
    Fetch an existing message.

    Returns:
        Message model, or None if not found.

    """
    return (
        db.query(models.Message)
        .filter(
            models.Message.id == message_id,
            models.Message.room_id == room_id,
        )
        .first()
    )


def read_messages(db: Session, room_id: UUID, skip: int = 0, limit: int | None = None) -> list[models.Message]:
    """
    Fetch all messages in a room.

    Returns:
        List of message models.

    """
    return db.query(models.Message).filter(models.Message.room_id == room_id).offset(skip).limit(limit).all()


def create_message(db: Session, message: schemas.Message, room_id: UUID) -> models.Message:
    """
    Create a new message.

    Returns:
        Newly-created message model.

    """
    # NOTE: This probably needs extra work
    db_message = models.Message(**message.dict(), room_id=room_id)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message


def update_message(db: Session, message: schemas.Message, room_id: UUID) -> models.Message:
    """
    Update a message.

    Returns:
        Updated message model.

    """
    (
        db.query(models.Message)
        .filter(
            models.Message.id == message.id,
            models.Message.room_id == room_id,
        )
        .update({
            "message": message.message,
            "last_edited": datetime.now(tz=timezone.utc),
        })
    )
    db.commit()
    return read_message(db, room_id=room_id, message_id=message.id)  # type: ignore[return-value]


def delete_message(db: Session, room_id: UUID, message_id: UUID) -> None:
    """Delete a message."""
    (
        db.query(models.Message)
        .filter(
            models.Message.id == message_id,
            models.Message.room_id == room_id,
        )
        .delete()
    )
    db.commit()


def update_user(db: Session, user: schemas.User) -> models.User:
    """
    Update a user.

    Returns:
        Updated user model.

    """
    (
        db.query(models.User)
        .filter(
            models.User.id == user.id,
            models.User.email == user.email,
        )
        .update({
            "username": user.username,
        })
    )
    db.commit()
    return read_user(db, user_id=user.id)  # type: ignore[return-value]


def delete_user(db: Session, user_id: UUID) -> None:
    """Delete a user."""
    (
        db.query(models.User)
        .filter(
            models.User.id == user_id,
        )
        .delete()
    )
    db.commit()
