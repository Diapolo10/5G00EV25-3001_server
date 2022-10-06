"""Implements user routes"""

import logging
from uuid import UUID

from fastapi import APIRouter, status

from server.schemas import User

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix='/users'
)


@router.post('/', status_code=status.HTTP_200_OK, response_model=User)
async def post_new_user(user: User):
    """Creates a new user"""

    logger.info("POST new user")
    return user


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
async def get_user_by_id(user_id: UUID):
    """Gets user by user ID"""

    logger.info("GET user %s", user_id)
    return User


@router.put('/{user_id}', status_code=status.HTTP_200_OK, response_model=User)
async def put_user_by_id(user_id: UUID):
    """Edits user by user ID"""

    logger.info("PUT user %s", user_id)
    return User


@router.delete('/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_by_id(user_id: UUID):
    """Deletes user by user ID"""

    logger.info("DELETE user %s", user_id)
