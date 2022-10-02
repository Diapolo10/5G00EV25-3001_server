"""Implements room routes"""

import logging
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from server import crud
from server.database import get_db
from server.schemas import Message, Room

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix='/rooms'
)


@router.get('/', status_code=status.HTTP_200_OK, response_model=list[Room])
async def get_public_rooms(db: Session = Depends(get_db)):
    """Fetches the public rooms"""

    logger.info("GET public chatrooms")

    rooms = crud.get_public_rooms(db)
    return rooms


@router.post('/', status_code=status.HTTP_200_OK, response_model=Room)
async def post_new_room(room: Room, db: Session = Depends(get_db)):
    """Creates a new room"""

    logger.info("POST new chatroom")

    if crud.get_room(db, room_id=room.id) is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Room already exists")
    db_room = crud.create_room(db, room=room)
    return db_room


@router.get('/{room_id}', status_code=status.HTTP_200_OK, response_model=Room)
async def get_room_by_id(room_id: UUID, db: Session = Depends(get_db)):
    """Fetches the specified room"""

    logger.info("GET chatroom by ID: %s", room_id)

    db_room = crud.get_room(db, room_id)
    if db_room is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")
    return db_room


@router.post('/{room_id}', status_code=status.HTTP_200_OK, response_model=Message)
async def post_message_by_id(room_id: UUID, message: Message, db: Session = Depends(get_db)):
    """Sends a message to the room"""

    logger.info("POST to chatroom ID: %s", room_id)

    # NOTE: Check if message exists first
    db_message = crud.create_message(db, message, room_id)
    return db_message


@router.delete('/{room_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_room_by_id(room_id: UUID, db: Session = Depends(get_db)):
    """Deletes the specified room"""

    logger.info("DELETE chatroom by ID: %s", room_id)


@router.get('/{room_id}/{message_id}', status_code=status.HTTP_200_OK, response_model=Message)
async def get_message_by_id(room_id: UUID, message_id: UUID, db: Session = Depends(get_db)):
    """Fetches the specified message"""

    logger.info("GET message by ID: %s", message_id)
    return Message


@router.put('/{room_id}/{message_id}', status_code=status.HTTP_200_OK, response_model=Message)
async def put_message_by_id(room_id: UUID, message_id: UUID, db: Session = Depends(get_db)):
    """Edits the specified message"""

    logger.info("PUT message by ID: %s", message_id)
    return Message


@router.delete('/{room_id}/{message_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_message_by_id(room_id: UUID, message_id: UUID, db: Session = Depends(get_db)):
    """Deletes the specified message"""

    logger.info("DELETE message by ID: %s", message_id)
