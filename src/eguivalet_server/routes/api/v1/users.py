"""Implements user routes."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Annotated
from uuid import UUID  # noqa: TC003

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session  # noqa: TC002

from eguivalet_server import crud
from eguivalet_server.database import get_db
from eguivalet_server.schemas import User, UserCreate

if TYPE_CHECKING:
    from eguivalet_server.models import User as UserModel

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/users",
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=User)
async def post_new_user(user: UserCreate, db: Annotated[Session, Depends(get_db)]) -> UserModel:
    """
    Create a new user.

    Raises:
        HTTPException: If the user ID or email exist.

    Returns:
        User object.

    """
    logger.info("POST new user")

    if crud.read_user(db, user_id=user.id) is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")
    if crud.read_user_by_email(db, email=user.email) is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")
    return crud.create_user(db, user=user)


@router.post("/login", status_code=status.HTTP_200_OK, response_model=User)
async def post_login_user(user: User) -> User:
    """
    Log the user in.

    Returns:
        User object.

    """
    logger.info("POST login user %s", user.username)
    return user


@router.post("/logout", status_code=status.HTTP_200_OK, response_model=User)
async def post_logout_user(user: User) -> User:
    """
    Log the user out.

    Returns:
        User object.

    """
    logger.info("POST logout user %s", user.username)
    return user


@router.get("/{user_id}", status_code=status.HTTP_200_OK, response_model=User)
async def get_user_by_id(user_id: UUID, db: Annotated[Session, Depends(get_db)]) -> UserModel:
    """
    Get user by user ID.

    Raises:
        HTTPException: If user does not exist.

    Returns:
        User object.

    """
    logger.info("GET user %s", user_id)

    db_user = crud.read_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return db_user


@router.put("/{user_id}", status_code=status.HTTP_200_OK, response_model=User)
async def update_user_by_id(user_id: UUID, user: User, db: Annotated[Session, Depends(get_db)]) -> UserModel:
    """
    Edit user by user ID.

    Raises:
        HTTPException: If the user does not exist.

    Returns:
        The updated user object.

    """
    logger.info("PUT user %s", user_id)

    db_user = crud.update_user(db, user=user)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return db_user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_by_id(user_id: UUID, db: Annotated[Session, Depends(get_db)]) -> None:
    """Delete user by user ID."""
    logger.info("DELETE user %s", user_id)

    crud.delete_user(db, user_id=user_id)
