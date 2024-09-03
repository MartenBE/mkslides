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
DEFAULT_CONFIG_LOCATION = "./assets/mkslides.default.yml"
EXPECTED_MARKDOWN_LOCATION = "./docs"
DEFAULT_OUTPUT_DIR = "./site"
