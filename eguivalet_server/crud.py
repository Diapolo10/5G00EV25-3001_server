"""C.R.U.D. - Create Read Update Delete"""

import logging
from datetime import datetime
from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from eguivalet_server import models, schemas

logger = logging.getLogger(__name__)


def read_public_rooms(db: Session) -> List[models.Room]:
    """Fetches all public rooms"""

    return (
        db.query(models.Room)
            .filter(models.Room.public == True)  # pylint: disable=C0121
            .all()
    )


def read_room(db: Session, room_id: UUID) -> Optional[models.Room]:
    """Fetches a room by the room ID"""

    return (
        db.query(models.Room)
            .filter(models.Room.id == room_id)
            .first()
    )


def create_room(db: Session, room: schemas.Room) -> models.Room:
    """Creates a new room"""

    db_room = models.Room(**room.dict())
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    return db_room


def delete_room(db: Session, room_id: UUID):
    """Deletes an existing room"""

    db.query(models.Room).filter(models.Room.id == room_id).delete()
    db.commit()


def read_user(db: Session, user_id: UUID) -> Optional[models.User]:
    """Gets a user by the user ID"""

    return (
        db.query(models.User)
            .filter(models.User.id == user_id)
            .first()
    )


def read_user_by_email(db: Session, email: str) -> Optional[models.User]:
    """Gets a user by the user email"""

    return (
        db.query(models.User)
            .filter(models.User.email == email)
            .first()
    )


def read_users(db: Session, skip: int = 0, limit: Optional[int] = None) -> List[models.User]:
    """Gets all users"""

    return (
        db.query(models.User)
            .offset(skip)
            .limit(limit)
            .all()
    )


def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    """Creates a new user"""

    fake_hashed_password = user.password.get_secret_value() + "generate_salt_here_and_hash"
    db_user = models.User(
        email=user.email,
        username=user.username,
        password_hash=fake_hashed_password
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def read_message(db: Session, room_id: UUID, message_id: UUID) -> Optional[models.Message]:
    """Fetches an existying message"""

    return (
        db.query(models.Message)
            .filter(
                models.Message.id == message_id,
                models.Message.room_id == room_id
            )
            .first()
    )


def read_messages(db: Session,
                  room_id: UUID,
                  skip: int = 0,
                  limit: Optional[int] = None) -> List[models.Message]:
    """Fetches all messages in a room"""

    return (
        db.query(models.Message)
            .filter(models.Message.room_id == room_id)
            .offset(skip)
            .limit(limit)
            .all()
    )


def create_message(db: Session, message: schemas.Message, room_id: UUID) -> models.Message:
    """Creates a new message"""

    # NOTE: This probably needs extra work
    db_message = models.Message(**message.dict(), room_id=room_id)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message


def update_message(db: Session, message: schemas.Message, room_id: UUID) -> models.Message:
    """Updates a message"""

    (
        db.query(models.Message)
            .filter(
                models.Message.id == message.id,
                models.Message.room_id == room_id
            )
            .update({
                'message': message.message,
                'last_edited': datetime.now()
            })
    )
    db.commit()
    return read_message(db, room_id=room_id, message_id=message.id)  # type: ignore[return-value]


def delete_message(db: Session, room_id: UUID, message_id: UUID):
    """Deletes a message"""

    (
        db.query(models.Message)
            .filter(
                models.Message.id == message_id,
                models.Message.room_id == room_id
            )
            .delete()
    )
    db.commit()


def update_user(db: Session, user: schemas.User) -> models.User:
    """Updates a user"""

    (
        db.query(models.User)
            .filter(
                models.User.id == user.id,
                models.User.email == user.email
            )
            .update({
                'username': user.username,
            })
    )
    db.commit()
    return read_user(db, user_id=user.id)  # type: ignore[return-value]


def delete_user(db: Session, user_id: UUID):
    """Deletes a user"""

    (
        db.query(models.User)
            .filter(
                models.User.id == user_id
            )
            .delete()
    )
    db.commit()
