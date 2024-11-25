import logging
import sys
import tempfile
from pathlib import Path

import click
from rich.logging import RichHandler

from .build import build
from .config import get_config
from .constants import (
    DEFAULT_OUTPUT_DIR,
    HIGHLIGHTJS_THEMES_VERSION,
    REVEALJS_VERSION,
    VERSION,
)

logger = logging.getLogger()
logger.setLevel("INFO")
logger.addHandler(RichHandler(show_path=False))

################################################################################

context_settings = {
    "help_option_names": ["-h", "--help"],
    "max_content_width": 120,
}

files_argument_data = {
    "metavar": "FILENAME|PATH",
    "type": click.Path(exists=True, resolve_path=True, path_type=Path),
}

config_file_argument_data = {
    "metavar": "FILENAME",
    "type": click.Path(exists=True, resolve_path=True, path_type=Path),
    "help": "Provide a specific MkSlides-Reveal config file.",
}


@click.group(context_settings=context_settings)
@click.version_option(
    VERSION,
    "-V",
    "--version",
    message=f"mkslides, version {VERSION}\nreveal.js, version {REVEALJS_VERSION}\nhighlight.js themes, version {HIGHLIGHTJS_THEMES_VERSION}"
    "",
)
@click.option(
    "-v",
    "--verbose",
    "verbose",
    help="Enable verbose output",
    is_flag=True,
)
def cli(verbose) -> None:
    """MkSlides - Slides with Markdown using the power of Reveal.js."""

    if verbose:
        logger.setLevel("DEBUG")
        logger.debug("Verbose output enabled")


# Build Command ################################################################


@cli.command(name="build")
@click.argument("files", **files_argument_data)  # type: ignore[arg-type]
@click.option("-f", "--config-file", **config_file_argument_data)  # type: ignore[arg-type]
@click.option(
    "-d",
    "--site-dir",
    type=click.Path(exists=True, resolve_path=True, path_type=Path),
    help="The directory to output the result of the slides build.",
    metavar="PATH",
    default=DEFAULT_OUTPUT_DIR,
)
def build_command(files: Path, config_file: Path | None, site_dir: str) -> None:
    """
    Build the MkDocs documentation.

    FILENAME|PATH is the path to the Markdown file, or the directory containing Markdown files.
    """
    logger.debug("Command: build")

    config = get_config(config_file)
    output_path = Path(site_dir).resolve(strict=False)

    build(config, files, output_path)


# Serve Command ################################################################


@cli.command(name="serve")
@click.argument("files", **files_argument_data)  # type: ignore[arg-type]
@click.option("-f", "--config-file", **config_file_argument_data)  # type: ignore[arg-type]
@click.option(
    "-a",
    "--dev-addr",
    help="IP address and port to serve slides locally.",
    metavar="<IP:PORT>",
    default="localhost:8000",
)
@click.option(
    "-o",
    "--open",
    "open_in_browser",
    help="Open the website in a Web browser after the initial build finishes.",
    is_flag=True,
)
@click.option(
    "--watch-index-theme",
    help="Include the index theme in list of files to watch for live reloading.",
    is_flag=True,
)
@click.option(
    "--watch-index-template",
    help="Include the index template in list of files to watch for live reloading.",
    is_flag=True,
)
@click.option(
    "--watch-slides-theme",
    help="Include the slides theme in list of files to watch for live reloading.",
    is_flag=True,
)
@click.option(
    "--watch-slides-template",
    help="Include the slides template in list of files to watch for live reloading.",
    is_flag=True,
)
def serve_command(  # noqa: C901
    files: Path,
    config_file: Path | None,
    dev_addr: str,
    open_in_browser: bool,
    watch_index_theme: bool,
    watch_index_template: bool,
    watch_slides_theme: bool,
    watch_slides_template: bool,
) -> None:
    """
    Run the builtin development server.

    FILENAME|PATH is the path to the Markdown file, or the directory containing Markdown files.
    """
    logger.debug("Command: serve")

    config = get_config(config_file)
    config.merge_with(
        {
            "serve": {
                "config_file": config_file,
                "dev_addr": dev_addr,
                "open_in_browser": open_in_browser,
                "watch_index_theme": watch_index_theme,
                "watch_index_template": watch_index_template,
                "watch_slides_theme": watch_slides_theme,
                "watch_slides_template": watch_slides_template,
            }
        }
    )
    output_path = Path(tempfile.mkdtemp(prefix="mkslides_")).resolve(strict=False)

    serve(
        config,
        files,
        output_path,
    )


################################################################################

if __name__ == "__main__":
    cli()
