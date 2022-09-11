"""Implements miscellaneous routes"""

import logging

from fastapi import APIRouter, Response, status
from fastapi.responses import PlainTextResponse

from server.schemas import HelloWorld
from server.config import ROBOTS_TXT

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get('/', status_code=status.HTTP_200_OK, response_model=HelloWorld)
async def get_root(response: Response):
    """A default route for testing"""

    logger.info("GET Hello World example")
    return {
        'hello': 'Hello, world!',
    }


@router.get('/robots.txt', status_code=status.HTTP_200_OK, response_class=PlainTextResponse)
async def get_robots_txt():
    """Gives the contents of robots.txt"""

    logger.info("GET robots.txt")
    return ROBOTS_TXT.read_text()
