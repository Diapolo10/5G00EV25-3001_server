"""Run if the package is executed like a command."""

import logging

import uvicorn

from eguivalet_server.config import (
    HOST,
    LOG_CONFIG,
    PORT,
)

uvicorn.run(
    "eguivalet_server.main:app",
    host=HOST,
    port=PORT,
    log_level=logging.INFO,
    reload=True,
    log_config=str(LOG_CONFIG),
    use_colors=True,
)
