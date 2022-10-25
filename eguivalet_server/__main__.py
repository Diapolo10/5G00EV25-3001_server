"""This script runs if the package is executed like a command"""

import logging

import uvicorn  # type: ignore

from eguivalet_server.config import (
    HOST,
    PORT,
    LOG_CONFIG,
)

uvicorn.run(
    'eguivalet_server.main:app',
    host=HOST,
    port=PORT,
    log_level=logging.INFO,
    reload=True,
    log_config=str(LOG_CONFIG),
    use_colors=True
)
