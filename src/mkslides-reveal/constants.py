from pathlib import Path
import re

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
DEFAULT_CONFIG_PATH = Path("./assets/mkslides.default.yml").resolve(strict=True)
DEFAULT_OUTPUT_DIR = "./site"

ASSETS_PATH = Path("assets").resolve(strict=True)
REVEALJS_PATH = Path(ASSETS_PATH / "reveal.js").resolve(strict=True)
HIGHLIGHTJS_THEMES_PATH = Path(ASSETS_PATH / "highlight.js" / "build").resolve(strict=True)
