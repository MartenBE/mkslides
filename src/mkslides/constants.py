import json
import re
from importlib import metadata, resources
from importlib.abc import Traversable
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, PackageLoader, select_autoescape

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

VERSION = metadata.version(__package__)
DEFAULT_CONFIG_LOCATION = Path("mkslides.yml")
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
