import re

from importlib import resources
from jinja2 import Environment, FileSystemLoader, PackageLoader, select_autoescape

MD_IMAGE_REGEX = re.compile(
    r"""
    !                           # Start of the image
    \[.*?\]                     # Alt text
    \((?P<location>.*?)\)       # Image location
    """,
    re.VERBOSE,
)
HTML_IMAGE_REGEX = re.compile(
    r"""
    <img                        # Start of the image
    .+?                         # Any attributes
    src=                        # src attribute
        (?P<delimiter>['\"])    # Delimiter
        (?P<location>.+?)       # Image location
        (?P=delimiter)          # Delimiter
    .*?                         # Any attributes
    >                           # End of the image
    """,
    re.VERBOSE,
)

HTML_BACKGROUND_IMAGE_REGEX = re.compile(
    r"""
    <!--                        # Start of the comment
    .*?                         # Any content
    data-background-image=      # data-background-image attribute
        (?P<delimiter>['\"])    # Delimiter
        (?P<location>.+?)       # Image location
        (?P=delimiter)          # Delimiter
    .*?                         # Any content
    -->                         # End of the comment
    """,
    re.VERBOSE,
)

EXPECTED_CONFIG_LOCATION = "mkslides.yml"
DEFAULT_OUTPUT_DIR = "site"

ASSETS_RESOURCE = resources.files("assets")
DEFAULT_CONFIG_RESOURCE = ASSETS_RESOURCE.joinpath("mkslides.default.yml")
REVEALJS_RESOURCE = ASSETS_RESOURCE.joinpath("reveal.js")
HIGHLIGHTJS_THEMES_RESOURCE = ASSETS_RESOURCE.joinpath("highlight.js", "build")

DEFAULT_JINJA2_ENVIRONMENT = Environment(
    loader=PackageLoader("assets"),
    autoescape=select_autoescape()
)

DEFAULT_INDEX_TEMPLATE = DEFAULT_JINJA2_ENVIRONMENT.get_template("index.html.jinja")
DEFAULT_SLIDESHOW_TEMPLATE = DEFAULT_JINJA2_ENVIRONMENT.get_template("slideshow.html.jinja")

LOCAL_JINJA2_ENVIRONMENT = Environment(loader=FileSystemLoader('.'))
