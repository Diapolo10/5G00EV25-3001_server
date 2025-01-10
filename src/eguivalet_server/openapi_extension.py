"""Extends OpenAPI to add enriched documentation."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from eguivalet_server.config import CODE_EXAMPLES, LABEL_LANG_MAPPING

if TYPE_CHECKING:
    from pathlib import Path

logger = logging.getLogger(__name__)


def add_examples(openapi_schema: dict, docs_dir: Path = CODE_EXAMPLES) -> dict:
    """
    Add code examples to the Redoc interface.

    Returns:
        A dictionary containing the OpenAPI schema updated with code examples.

    """
    path_key = "paths"
    code_key = "x-codeSamples"

    for folder in docs_dir.iterdir():
        if folder.is_file():
            continue
        files = [f for f in folder.iterdir() if f.is_file()]
        for file in files:
            parts = file.name.split("-")
            if len(parts) >= 1:
                route = "/"
                if len(parts) >= 2:  # noqa: PLR2004
                    route += "/".join(parts[:-1])
                    if not parts[-2].endswith("}"):
                        route += "/"
                method = parts[-1].split(".")[0]
                logger.info(
                    "[%s][%s][%s][%s]",
                    path_key,
                    route,
                    method,
                    code_key,
                )

                if route in openapi_schema[path_key]:
                    if code_key not in openapi_schema[path_key][route][method]:
                        openapi_schema[path_key][route][method].update({code_key: []})

                    openapi_schema[path_key][route][method][code_key].append({
                        "lang": LABEL_LANG_MAPPING[folder.name],
                        "source": file.read_text(),
                        "label": LABEL_LANG_MAPPING[folder.name],
                    })
                else:
                    logger.error("Error adding code example to OpenAPI; %s", file)

    return openapi_schema
