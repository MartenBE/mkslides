# SPDX-FileCopyrightText: Copyright (C) 2024 Martijn Saelens and Contributors to the project (https://github.com/MartenBE/mkslides/graphs/contributors)
#
# SPDX-License-Identifier: MIT

import json
import logging
import re
from importlib import metadata, resources
from importlib.resources.abc import Traversable
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, PackageLoader, select_autoescape

logger = logging.getLogger(__name__)

################################################################################


def gather_themes(resource: Traversable) -> list[str]:
    theme_names = []
    for theme in resource.iterdir():
        if theme.is_file():
            theme_path = Path(theme.name)
            if theme_path.suffix == ".css":
                theme_names.append(theme_path.stem)

    return theme_names


################################################################################

HTML_BACKGROUND_IMAGE_REGEX = re.compile(
    r"""
    data-background-image=      # data-background-image attribute
        (?P<delimiter>['\"])    # Delimiter
        (?P<location>.+?)       # Image location
        (?P=delimiter)          # Delimiter
    """,
    re.VERBOSE,
)

MD_RELATIVE_SLIDESHOW_LINK_REGEX = re.compile(
    r"""
    \[(?P<alt_text>.*?)\]               # Alt text
    \((?P<location>.+?\.[mM][dD])\)     # Image location
    """,
    re.VERBOSE,
)

HTML_RELATIVE_SLIDESHOW_LINK_REGEX = re.compile(
    r"""
    <a                                  # Start of the image
    .+?                                 # Any attributes
    href=                               # src attribute
        (?P<delimiter>['\"])            # Delimiter
        (?P<location>.+?\.[mM][dD])     # Image location
        (?P=delimiter)                  # Delimiter
    .*?                                 # Any attributes
    >                                   # End of the image
    """,
    re.VERBOSE,
)

MD_EXTENSION_REGEX = re.compile(r"\.[mM][dD]$")

VERSION = metadata.version(__package__)
DEFAULT_CONFIG_LOCATION = Path("mkslides.yml")
DEFAULT_INPUT_DIR = "slides"
DEFAULT_INPUT_DIR2 = "docs"
DEFAULT_OUTPUT_DIR = "site"

ASSETS_RESOURCE = resources.files(__package__).joinpath("assets")

REVEALJS_RESOURCE = ASSETS_RESOURCE.joinpath("reveal.js")
REVEALJS_THEMES_RESOURCE = REVEALJS_RESOURCE.joinpath("dist", "theme")
REVEALJS_THEMES_LIST = gather_themes(REVEALJS_THEMES_RESOURCE)
REVEALJS_VERSION = None
with REVEALJS_RESOURCE.joinpath("package.json").open(encoding="utf-8-sig") as f:
    REVEALJS_VERSION = json.load(f)["version"]

HIGHLIGHTJS_RESOURCE = ASSETS_RESOURCE.joinpath("highlight.js")
HIGHLIGHTJS_THEMES_RESOURCE = HIGHLIGHTJS_RESOURCE.joinpath("build", "styles")
HIGHLIGHTJS_THEMES_LIST = gather_themes(HIGHLIGHTJS_THEMES_RESOURCE)

HIGHLIGHTJS_THEMES_VERSION = None
with HIGHLIGHTJS_RESOURCE.joinpath("build", "package.json").open(
    encoding="utf-8-sig",
) as f:
    HIGHLIGHTJS_THEMES_VERSION = json.load(f)["version"]

DEFAULT_JINJA2_ENVIRONMENT = Environment(
    loader=PackageLoader(__package__, "assets/templates"),
    autoescape=select_autoescape(),
)
DEFAULT_INDEX_TEMPLATE = DEFAULT_JINJA2_ENVIRONMENT.get_template("index.html.jinja")
DEFAULT_SLIDESHOW_TEMPLATE = DEFAULT_JINJA2_ENVIRONMENT.get_template(
    "slideshow.html.jinja",
)
LOCAL_JINJA2_ENVIRONMENT = Environment(loader=FileSystemLoader("."), autoescape=True)

OUTPUT_ASSETS_DIRNAME: str = "mkslides-assets"
