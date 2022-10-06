"""Implements API v1 routes"""

import logging

from fastapi import APIRouter

from server.routes.api.v1 import db, management, rooms, users

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix='/v1',
)

router.include_router(db.router)
router.include_router(management.router)
router.include_router(rooms.router)
router.include_router(users.router)
