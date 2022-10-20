# EguiValet Server - Documentation - Index

This document contains the documentation for the EguiValet Server project.

## Table of Contents

- [EguiValet Server - Documentation - Index](#eguivalet-server---documentation---index)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Installation](#installation)
  - [Development](#development)
    - [Project file structure](#project-file-structure)
      - [Root directory](#root-directory)
      - [Docs](#docs)
      - [Source directory](#source-directory)
      - [Tests](#tests)
    - [OpenAPI docs](#openapi-docs)

## Introduction

This is the server half of the EguiValet chat application project, which
functions as the brains behing the chat system, storing chatrooms, users,
and messages, and handling how they're received and sent between clients.

The server has beeen designed to run on all major operating systems in order
to make development easier, even if it only really needs to run on Linux-based
systems.

The server is thoroughly unit-tested and has good test coverage. Furthermore,
it has been designed with robustness and reusability in mind. All of thesee
factors together enable rapid, fearless prototyping, as any major problems
should be caught by the existing test suite.

This guide will instruct you on how to operate the server application, how to
extend it, where to find what, and the last chapter will provide help for
solving known problems.

## Installation

To install the server application, it is recommended to download the latest
packaged executable file from the project's
[GitHub releases section][GitHub Releases] as that simplifies the installation
process.

1. Download the latest executable file
2. Run the executable to launch the server

If one doesn't exist, you'll likely need to install from source.

1. Install [Python] version 3.8 or newer (if not already installed)
2. Download the [project's Git repository][GitHub]

    ```shell
    # This will work on all platforms if you don't want to use the GUI
    cd ~
    curl -LO https://github.com/Diapolo10/5G00EV25-3001_server/archive/refs/heads/main.zip -o main.zip
    ```

3. Unpack the downloaded ZIP-file to a convenient location
4. Open a command line session in the location, and run

    ```shell
    pip3 install poetry
    python3 -m poetry install
    python3 -m poetry shell
    ```

    to install the dependencies and to open a virtual environment session

## Development

This part of the documentation will instruct you on how the project is
structured, and how to continue developing it.

### Project file structure

The project files can be categorised roughly into four categories; the project
metadata files in the root directory, files in the documentation directory,
the project source code in its directory, and tthe automated tests. This part
of the documentation will attempt to proovide an overview of all these.

```text
📂root
 ┣ 📂.github
 ┣ 📂docs
 ┣ 📦equivalet_server
 ┣ 📂tests
 ┣ 📜.gitattributes
 ┣ 📜.gitignore
 ┣ 📜.markdownlint.jsonc
 ┣ 📜CHANGELOG.md
 ┣ 📜CODE_OF_CONDUCT.md
 ┣ 📜CONTRIBUTING.md
 ┣ 📜LICENSE
 ┣ 📜logging.conf
 ┣ 📜Makefile
 ┣ 📜poetry.lock
 ┣ 📜pyproject.toml
 ┣ 📜README.md
 ┗ 📜server.db
```

#### Root directory

The repository houses several metadata files which are mostly either
information about the project itself, configuration files, or utility
files.

- `.gitattributes`
    Tells Git how certain kinds of files should be treated when checking for
    differences, for instance

- `.gitignore`
    Contains files annd filename patterns that should be excluded from the Git
    repository

- `.markdownlint.jsonc`
    Configures Markdown linters too use custom general rules

- `CHANGELOG.md`
    This file documents all meaningful changes made to the project. It is
    updated by hand, so sometimes changes may slip by, but it nevertheless
    offers a goood overview regarding what changes have been made over time

- `CODE_OF_CONDUCT.md`
    This file describes how people working on the project should
    conduct themselves. OOr, in other words, it's a guide for decent behaviour.
    Commonly used in open-source projects

- `CONTRIBUTING.md`
    Contains a rough overview on how to contribute to the project

- `LICENSE`
    Contains the licensing information for the project, in this case a copy of
    the MIT license

- `logging.conf`
    Contains the coonfiguration for the server's logger

- `Makefile`
    Makes the project easier to install and use on Unix-like systems

- `poetry.lock`
    Contains 'frozen' dependency versions, enabling repeatable builds where
    each uses the same exact dependency versions. Is not meant to be modified
    by hand

- `pyproject.toml`
    Coontains most of the metadata regarding the source code, from runtime and
    development dependencies too the project version number, configuration for
    linters and unit tests, and information regarding what to include in
    releases

- `README.md`
    Contains a brief overview of the project, with links to the documentation,
    the GitHub project, and other general information

- `server.db`
    Generated by the server if it doesn't already exist. This is an SQLite
    database that is currently used to store the server state - this could
    change in the future. It can be viewed manually with a tool such as
    [DB Browser]

#### Docs

The `docs` directory mostly contains the documentation, which you are reading
right now, but in addition it also houses code examples for different API
requests using different languages. These examples are shown on the Redoc API
interface.

```text
📂docs
 ┣ 📂example_code
 ┣ 📜index.md
 ┗ 📜pull_request_template.md
```

#### Source directory

The directory containing the project's source code, `eguivalet_server`, is
fairly vast. There's likely no need to go into full detail as the files are
mostly self-documenting, so this section aims to provide a general overview.

```text
📦equivalet_server
 ┣ 📂routes
 ┃ ┣ 📂api
 ┃ ┃ ┣ 📂v1
 ┃ ┃ ┃ ┣ 📜__init__.py
 ┃ ┃ ┃ ┣ 📜rooms.py
 ┃ ┃ ┃ ┗ 📜users.py
 ┃ ┃ ┗ 📜__init__.py
 ┃ ┣ 📜__init__.py
 ┃ ┣ 📜other.py
 ┃ ┗ 📜robots.txt
 ┣ 📜__init__.py
 ┣ 📜config.py
 ┣ 📜crud.py
 ┣ 📜database.py
 ┣ 📜main.py
 ┣ 📜models.py
 ┣ 📜openapi_extension.py
 ┣ 📜schemas.py
 ┗ 📜utility.py
```

- `routes`
  This directory contains the different routes proovided by the server API.
  The directory structure is made to resemble the API call URLs on purpose,
  to make it easier to associate API paths with the files managing them.

  The `__init__.py`-files exist to have the directories act like parts of
  the API path and to include the individual files up the stack. Adding a new
  file with API paths requires you to edit the `__init__.py`-file in that
  directory for FastAPI to recognise it.

  The API version is its own directory to make it easy to develop a new API
  version in the future alongside the existing one.

  The route files themselves are fairly self-explanatory, but in a nutshell,

  - `rooms.py` contains routes for chatrooms
  - `users.py` contains routes for user management
  - `other.py` contains miscellaneous routes, like the Hello World message
  - `robots.txt` contains what the API serves when asked for it

- `config.py`
  Contains

- `crud.py`
- `database.py`
- `main.py`
- `models.py`
- `openapi_extension.py`
- `schemas.py`
- `utility.py`

#### Tests

The `tests`-directory coontains unit tests - how original. But that's actually
not everything, which is why this directory deserves its own coverage.

### OpenAPI docs

Thanks to `fastapi`, the EguiValet server offers built-in API documentation in
the form of Redoc and Swagger. They are useful tools for keeping track of which
routes

[DB Browser]: https://sqlitebrowser.org/
[GitHub]: https://github.com/Diapolo10/5G00EV25-3001_server
[GitHub Releases]: https://github.com/Diapolo10/5G00EV25-3001_server/releases
[Python]: https://www.python.org/downloads/

<!-- markdownlint-configure-file {
    "MD013": false
} -->
<!--
    MD013: Line length
-->
