"""Implements API routes"""

import logging

from fastapi import APIRouter

from eguivalet_server.routes.api import v1

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix='/api',
)

router.include_router(v1.router)
