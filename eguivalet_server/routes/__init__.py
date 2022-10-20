"""Implements routes"""

import logging

from fastapi import APIRouter

from eguivalet_server.routes import api, other

logger = logging.getLogger(__name__)

router = APIRouter()

router.include_router(api.router)
router.include_router(other.router)
