"""C.R.U.D. - Create Read Update Delete"""

import logging
from uuid import UUID

from sqlalchemy.orm import Session

from server import models, schemas

logger = logging.getLogger(__name__)


def get_public_rooms(db: Session):
    """Fetches all public rooms"""

    return db.query(models.Room).filter(models.Room.public is True).all()


def get_room(db: Session, room_id: UUID):
    """Fetches a room by the room ID"""

    return db.query(models.Room).filter(models.Room.id == room_id).first()


def create_room(db: Session, room: schemas.Room):
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


def get_user(db: Session, user_id: UUID):
    """Gets a user by the user ID"""

    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    """Gets a user by the user email"""

    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    """Gets all users"""

    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
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


def create_message(db: Session, message: schemas.Message, room_id: UUID):  # pylint: disable=W0613
    """Creates a new message"""

    db_message = models.Message(**message.dict())  # NOTE: This probably needs extra work
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message
