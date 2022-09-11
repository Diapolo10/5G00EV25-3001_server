"""Contains implementations for Pydantic models used in the API"""

# pylint: disable=missing-class-docstring

import logging

from pydantic import BaseModel

logger = logging.getLogger(__name__)


class HelloWorld(BaseModel):
    """Hello, world!"""

    hello: str
