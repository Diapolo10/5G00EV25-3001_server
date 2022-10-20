"""Implements API v1 routes"""

import logging

from fastapi import APIRouter

from eguivalet_server.routes.api.v1 import rooms, users

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix='/v1',
)

router.include_router(rooms.router)
router.include_router(users.router)
