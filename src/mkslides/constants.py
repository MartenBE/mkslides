import json
import re
from importlib import metadata, resources

from jinja2 import Environment, FileSystemLoader, PackageLoader, select_autoescape

HTML_BACKGROUND_IMAGE_REGEX = re.compile(
    r"""
    data-background-image=      # data-background-image attribute
        (?P<delimiter>['\"])    # Delimiter
        (?P<location>.+?)       # Image location
        (?P=delimiter)          # Delimiter
    """,
    re.VERBOSE,
)

EXPECTED_CONFIG_LOCATION = "mkslides.yml"
DEFAULT_OUTPUT_DIR = "site"

ASSETS_RESOURCE = resources.files("assets")
DEFAULT_CONFIG_RESOURCE = ASSETS_RESOURCE.joinpath("mkslides.default.yml")
REVEALJS_RESOURCE = ASSETS_RESOURCE.joinpath("reveal.js")
REVEALJS_THEMES_RESOURCE = REVEALJS_RESOURCE.joinpath("dist", "theme")
HIGHLIGHTJS_RESOURCE = ASSETS_RESOURCE.joinpath("highlight.js")
HIGHLIGHTJS_THEMES_RESOURCE = HIGHLIGHTJS_RESOURCE.joinpath("build", "styles")

DEFAULT_JINJA2_ENVIRONMENT = Environment(
    loader=PackageLoader("assets"),
    autoescape=select_autoescape(),
)
DEFAULT_INDEX_TEMPLATE = DEFAULT_JINJA2_ENVIRONMENT.get_template("index.html.jinja")
DEFAULT_SLIDESHOW_TEMPLATE = DEFAULT_JINJA2_ENVIRONMENT.get_template(
    "slideshow.html.jinja",
)
LOCAL_JINJA2_ENVIRONMENT = Environment(loader=FileSystemLoader("."), autoescape=True)

VERSION = metadata.version("mkslides")

REVEALJS_VERSION = None
with REVEALJS_RESOURCE.joinpath("package.json").open(encoding="utf-8-sig") as f:
    REVEALJS_VERSION = json.load(f)["version"]

HIGHLIGHTJS_THEMES_VERSION = None
with HIGHLIGHTJS_RESOURCE.joinpath("build", "package.json").open(
    encoding="utf-8-sig",
) as f:
    HIGHLIGHTJS_THEMES_VERSION = json.load(f)["version"]
