"""Implements API v1 routes"""

import logging

from fastapi import APIRouter

from eguivalet_server.routes.api.v1 import rooms, users
from eguivalet_server.schemas import UserCreate, UserRead

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix='/v1',
)

router.include_router(rooms.router)
router.include_router(users.router)

router.include_router(
    users.fastapi_users.get_auth_router(users.auth_backend), prefix="/auth/jwt", tags=["auth"],
)
router.include_router(
    users.fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
router.include_router(
    users.fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
router.include_router(
    users.fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)
