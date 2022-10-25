# EguiValet Server - Documentation - Index <!-- omit in toc -->

This document contains the documentation for the EguiValet Server project.

## Table of Contents <!-- omit in toc -->

- [1. Introduction](#1-introduction)
- [2. Installation](#2-installation)
- [3. Development](#3-development)
  - [3.1. Project file structure](#31-project-file-structure)
    - [3.1.1. Root directory](#311-root-directory)
    - [3.1.2. Docs](#312-docs)
    - [3.1.3. Source directory](#313-source-directory)
    - [3.1.4. Tests](#314-tests)
  - [3.2. OpenAPI docs](#32-openapi-docs)
  - [3.3. Unit tests](#33-unit-tests)
  - [3.4. Linters](#34-linters)
  - [3.5. Build](#35-build)
- [4. Usage](#4-usage)
  - [4.1. Running](#41-running)
- [5. Troubleshooting](#5-troubleshooting)

## 1. Introduction

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

## 2. Installation

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

## 3. Development

This part of the documentation will instruct you on how the project is
structured, and how to continue developing it.

### 3.1. Project file structure

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

#### 3.1.1. Root directory

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

#### 3.1.2. Docs

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

#### 3.1.3. Source directory

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

- `__main__.py`
  This file makes the module an executable Python package
  (eg. `python -m eguivalet_server`)

- `config.py`
  Contains virtually all important configuration options for the server,
  such as string data length limits and the database URL, which can be
  changed if needed

- `crud.py`
  Utilities for interfacing with the database. The name stands for
  Create, Read, Update, Delete

- `database.py`
  Defines the database engine, and a function that auto-closes a provided
  database session

- `main.py`
  The main executable used to run the program

- `models.py`
  Defines SQLAlchemy database models

- `openapi_extension.py`
  Defines extensions for the OpenAPI standard, too enrich the content of
  Redoc and Swagger UI

- `schemas.py`
  Defines Pydantic schemas for automatic data verification and conversion

- `utility.py`
  Defines miscellaneous utility functions that don't really fit elsewhere

#### 3.1.4. Tests

The `tests`-directory contains unit tests - how original. But that's actually
not everything, which is why this directory deserves its own coverage.

```text
📂tests
 ┣ 📂reports
 ┃ ┣ 📂coverage-html
 ┃ ┗ 📜coverage.xml
 ┣ 📜conftest.py
 ┣ 📜test_crud.py
 ┣ 📜test_rooms.py
 ┣ 📜test_root.py
 ┣ 📜test_schemas.py
 ┣ 📜test_users.py
 ┗ 📜test.db
```

- `reports`
  This directory is generated whenever unit tests are executed, containing
  coverage reports in both JUnit XML and HTML format, thee latter being a
  human-readable web page

- `conftest.py`
  This is a special file `pytest` loads when it starts a test session. In
  this project, it's used to define useful fixtures for getting access to a
  testing database, and initialising it for different test configurations

- `test_crud.py`
  Contains unit tests for CRUD operations not already covered by other tests

- `test_rooms.py`
  Contains unit tests for chatroom routes

- `test_root.py`
  Contains unit tests for the "other" routes for the root address, like
  the Hello World message

- `test_schemas.py`
  Contains unit tests for Pydantic schemas not already covered by other tests

- `test_users.py`
  Contains unit ttests for user routes

- `test.db`
  This is a database file generated while running the tests. In practice,
  the database remains empty as the tests utilise transactions which are
  ultimately cancelled, but it neeeds to exist during testing - in the
  future the test suite may delete it automatically after the tests finish

### 3.2. OpenAPI docs

Thanks to `fastapi`, the EguiValet server offers built-in API documentation in
the form of Redoc and Swagger. They are useful tools for keeping track of which
routes the API defines, what HTTP methods they support, what kind of data they
expect and return, and even what errors may arise.

Swagger is a flexible interface, letting you make requests to the API from
within itself, if you want to test something on the fly. Assuming default
configuration, it can be accessed using a web browser while the server is
running via the address

```text
localhost:11037/docs
```

Swagger is very intuitive to use, so it shouldn't require additional
explanation.

Redoc is purely for API documentation, and can display more information than
Swagger. It can be accessed via the address

```text
localhost:11037/redoc
```

### 3.3. Unit tests

All of the unit tests for the project are contained in `/tests`. They use
`pytest`, but it is possible to write tests using the built-in `unittest`
module as well since `pytest` supports it. That said, it is recommended to
stick to `pytest` as fragmenting the test codebase would not be ideal.

The existing test suite can be used as an example for writing new tests, in
fact that is encouraged in order to keep the tests uniform.

Running the unit tests is as simplle as running the command `poetry run pytest`
in a terminal, such as PowerShell, within the project's root directory.

The unit tests generate coverage reports, which can be used to track how much
of the codebase was executed during testing. This is a useful metric, and a
good goal is 90% coverage or better. These reports are automatically uploaded
to Codecov when pushing code to GitHub, and can be seen on the `README.md`.

### 3.4. Linters

Linters are used to keep the codebase consistent and as compliant to the PEP-8
and PEP-257 rules as possible. Sometimes they cannot be perfectly met due to
design considerations, which is normal, but it is a goood aim to always focus
on writing readable and maintainable, consistent code.

The project uses `pylint` and `flake8`, both of which are configured in
`pyproject.toml`. To run them, simply run

```sh
poetry run pylint eguivalet_server
poetry run pflake8
```

in a terminal, such as PowerShell, within the project's root directory.

> The `p` in `pflake8` is not a typo. In order to keep `flake8`'s configuration
in `pyproject.toml`, until official support is added we use `pyproject-flake8`
as a middleman, which uses that alias.

Running the linters will list all places where they find style problems,
letting you fix them at your leisure. If a problem cannot be fixed due to a
design consideration for the project, either ignore that one line or add an
exception in `pyproject.toml` to ignore the error altogether, preferably
with some kind of an explanation.

### 3.5. Build

Building the project is, again, fairly simple. By running
`poetry build --format wheel` in a terminal, Poetry will generate a portable
wheel file which can then be easily installed anywhere with a compatible Python
environment and an internet connection for fetching the dependencies. The
generated file can be found in `/dist`.

## 4. Usage

The EguiValet server has beeen designed to be fairly easy to use without any
mandatory training.

### 4.1. Running

If using a cloned repository, you simply need to run the main program while
Poetry's virtual environment is active.

1. Install a compatible Python version (3.8 or newer at the time of writing)
2. Install Poetry (`pip install poetry`)
   NOTE: If Python wasn't addeed to PATH during installlation, you may need to
   prepend all these commands with `py -m` for them to work.
3. While in the project directory, run `poetry shell`
4. After the virtual environment has been generated, run `poetry install` to
   install all dependencies. If you don't care about development dependencies,
   you can add the `--no-dev` flag
5. Once all dependencies have been installed, simply run
   `poetry run python eguivalet_server/main.py` within the environment

This will launch Uvicorn, which begins seetting up the server and it should
finish in a minute. All the logs will be displayed in the terminal. You can
test it works by trying to open

```text
localhost:11037/
```

in any web browser on your computer. A message should get logged into the
terminal.

Once the server is running, nothing needs to be done unlless you need to
reconfigure the server or perform other administrative tasks.

## 5. Troubleshooting

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
