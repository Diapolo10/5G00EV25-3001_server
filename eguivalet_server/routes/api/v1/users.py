"""Implements user routes"""

import logging
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from eguivalet_server import crud
from eguivalet_server.database import get_db
from eguivalet_server.schemas import User, UserCreate

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix='/users'
)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=User)
async def post_new_user(user: UserCreate, db: Session = Depends(get_db)):
    """Creates a new user"""

    logger.info("POST new user")

    if crud.read_user(db, user_id=user.id) is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")
    if crud.read_user_by_email(db, email=user.email) is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")
    db_user = crud.create_user(db, user=user)
    return db_user


@router.post('/login', status_code=status.HTTP_200_OK, response_model=User)
async def post_login_user(user: User):
    """Logs the user in"""

    logger.info("POST login user %s", user.username)
    return user


@router.post('/logout', status_code=status.HTTP_200_OK, response_model=User)
async def post_logout_user(user: User):
    """Logs the user out"""

    logger.info("POST logout user %s", user.username)
    return user


@router.get('/{user_id}', status_code=status.HTTP_200_OK, response_model=User)
async def get_user_by_id(user_id: UUID, db: Session = Depends(get_db)):
    """Gets user by user ID"""

    logger.info("GET user %s", user_id)

    db_user = crud.read_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return db_user


@router.put('/{user_id}', status_code=status.HTTP_200_OK, response_model=User)
async def update_user_by_id(user_id: UUID, user: User, db: Session = Depends(get_db)):
    """Edits user by user ID"""

    logger.info("PUT user %s", user_id)

    db_user = crud.update_user(db, user=user)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return db_user


@router.delete('/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_by_id(user_id: UUID, db: Session = Depends(get_db)):
    """Deletes user by user ID"""

    logger.info("DELETE user %s", user_id)

    crud.delete_user(db, user_id=user_id)
