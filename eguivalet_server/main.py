"""Launches the messaging service"""

import logging
import logging.config
import sys

import tomli
import uvicorn  # type: ignore
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

from eguivalet_server import models
from eguivalet_server.config import (
    HOST,
    PORT,
    LOG_CONFIG,
    PYPROJECT_TOML,
)
from eguivalet_server.database import engine
from eguivalet_server.openapi_extension import add_examples
from eguivalet_server.routes import router

project_metadata = tomli.loads(PYPROJECT_TOML.read_text())


# Setup loggers
logging.config.fileConfig(LOG_CONFIG, disable_existing_loggers=False)
logger = logging.getLogger(__name__)

if "pytest" not in sys.modules:
    # Initialise the main database
    logger.info("Initialising database")
    models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    swagger_ui_parameters={
        'filter': True,
        'syntaxHighlight.theme': 'arta',
    },
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['GET', 'POST', 'PUT', 'DELETE'],
    allow_headers=['*'],
)

app.include_router(router)


def custom_openapi():
    """Applies code examples to Redoc"""

    if app.openapi_schema:
        return app.openapi_schema

    poetry = project_metadata['tool']['poetry']

    openapi_schema = get_openapi(
        title="Messaging Service Server",
        version=poetry['version'],
        description=poetry['description'],
        routes=app.routes
    )
    openapi_schema['info']['x-logo'] = {
        'url': 'https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png',
    }

    app.openapi_schema = add_examples(openapi_schema)

    return app.openapi_schema


app.openapi = custom_openapi  # type: ignore

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host=HOST,
        port=PORT,
        reload=True,
        log_level=logging.INFO,
        log_config=str(LOG_CONFIG),
        use_colors=True
    )
