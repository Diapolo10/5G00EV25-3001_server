"""This file contains the global configuration settings for the program"""

import re
from enum import IntEnum, auto
from pathlib import Path


# Common

PROJECT_DIR = Path(__file__).parent
ROOT_DIR = PROJECT_DIR.parent
DOCS_DIR = ROOT_DIR / 'docs'
CODE_EXAMPLES = DOCS_DIR / 'example_code'

LOG_CONFIG = ROOT_DIR / 'logging.conf'
PYPROJECT_TOML = ROOT_DIR / 'pyproject.toml'
ROBOTS_TXT = PROJECT_DIR / 'routes' / 'robots.txt'


# Chat

MAX_MESSAGE_LENGTH = 256
MIN_MESSAGE_LENGTH = 1
MAX_USERNAME_LENGTH = 64
MIN_USERNAME_LENGTH = 1
MAX_EMAIL_ADDRESS_LENGTH = 255
MIN_EMAIL_ADDRESS_LENGTH = 3
MAX_PASSWORD_HASH_LENGTH = 128


# Database

SQLALCHEMY_DATABASE_URL = 'sqlite:///./server.db'
SQLALCHEMY_TEST_DATABASE_URL = 'sqlite:///./tests/test.db'
# SQLALCHEMY_DATABASE_USERNAME = 'user'
# SQLALCHEMY_DATABASE_PASSWORD = 'password'  # If used, this should be an environmental variable
# SQLALCHEMY_DATABASE_URL = (
#     'postgresql://'
#     f'{SQLALCHEMY_DATABASE_USERNAME}:{SQLALCHEMY_DATABASE_PASSWORD}'
#     '@postgresserver/db'
# )


# Enums

class AccessLevel(IntEnum):
    """Contains different access levels for users"""

    BANNED = auto()
    BASIC = auto()
    VERIFIED = auto()
    MODERATOR = auto()
    ADMINISTRATOR = auto()


# Running

HOST = '127.0.0.1'
PORT = 11037
URL = f'http://{HOST}:{PORT}'


# Regular expressions

ANY_REGEX = re.compile(r'^.*$')
SEM_VER_REGEX = re.compile(
    r'''
        (0|[1-9][0-9]*)\.  # Major
        (0|[1-9][0-9]*)\.  # Minor
        (0|[1-9][0-9]*)    # Patch
        (?:-((?:0|[1-9][0-9]*|[0-9]*[a-zA-Z-][0-9a-zA-Z]*)
        (?:\.(?:0|[1-9][0-9]*|[0-9]*[a-zA-Z-][0-9a-zA-Z]*))*))?  # Pre-release
        (?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?               # Build
    ''',
    re.VERBOSE
)


# Unit tests

USER_ROOT = '/api/v1/users'
ROOM_ROOT = '/api/v1/rooms'


# OpenAPI

LABEL_LANG_MAPPING = {
    'JavaScript': 'JavaScript',
    'Rust': 'Rust',
}
