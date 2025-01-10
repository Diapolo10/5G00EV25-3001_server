"""Implements miscellaneous routes."""

import logging

from fastapi import APIRouter, status
from fastapi.responses import PlainTextResponse

from eguivalet_server.config import ROBOTS_TXT
from eguivalet_server.schemas import HelloWorld

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/", status_code=status.HTTP_200_OK, response_model=HelloWorld)
async def get_root() -> dict[str, str]:
    """
    Define example route.

    Returns:
        A Hello World JSON response.

    """
    logger.info("GET Hello World example")
    return {
        "hello": "Hello, world!",
    }


@router.get("/robots.txt", status_code=status.HTTP_200_OK, response_class=PlainTextResponse)
async def get_robots_txt() -> str:
    """
    Give the contents of robots.txt.

    Returns:
        A string containing the contents of the robots.txt file.

    """
    logger.info("GET robots.txt")
    return ROBOTS_TXT.read_text()
