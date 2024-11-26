import logging
import tempfile
from pathlib import Path

import click
from omegaconf import OmegaConf
from rich.logging import RichHandler

from mkslides.serve import serve
from mkslides.utils import parse_ip_port

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

files_argument_data = {
    "metavar": "FILENAME|PATH",
    "type": click.Path(exists=True, resolve_path=True, path_type=Path),
}

config_file_argument_data = {
    "metavar": "FILENAME",
    "type": click.Path(exists=True, resolve_path=True, path_type=Path),
    "help": "Provide a specific MkSlides-Reveal config file.",
}

strict_argument_data = {
    "is_flag": True,
    "help": "Fail if a relative link cannot be resolved, otherwise just print a warning.",
}


@click.group(
    context_settings={
        "help_option_names": ["-h", "--help"],
        "max_content_width": 120,
    },
)
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
def cli(verbose: bool) -> None:
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
    type=click.Path(path_type=Path),
    help="The directory to output the result of the slides build.",
    metavar="PATH",
    default=DEFAULT_OUTPUT_DIR,
)
@click.option("-s", "--strict", **strict_argument_data)  # type: ignore[arg-type]
def build_command(
    files: Path,
    config_file: Path | None,
    site_dir: str,
    strict: bool,
) -> None:
    """
    Build the MkDocs documentation.

    FILENAME|PATH is the path to the Markdown file, or the directory containing Markdown files.
    """
    logger.debug("Command: build")

    config = get_config(config_file)
    output_path = Path(site_dir).resolve(strict=False)

    build(config, files, output_path, strict)


# Serve Command ################################################################


@cli.command(name="serve")
@click.argument("files", **files_argument_data)  # type: ignore[arg-type]
@click.option("-f", "--config-file", **config_file_argument_data)  # type: ignore[arg-type]
@click.option("-s", "--strict", **strict_argument_data)  # type: ignore[arg-type]
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
def serve_command(
    files: Path,
    config_file: Path | None,
    strict: bool,
    dev_addr: str,
    open_in_browser: bool,
) -> None:
    """
    Run the builtin development server.

    FILENAME|PATH is the path to the Markdown file, or the directory containing Markdown files.
    """
    logger.debug("Command: serve")

    config = get_config(config_file)
    output_path = Path(tempfile.mkdtemp(prefix="mkslides_")).resolve(strict=False)
    dev_ip, dev_port = parse_ip_port(dev_addr)
    serve_config = OmegaConf.structured(
        {
            "dev_ip": dev_ip,
            "dev_port": dev_port,
            "open_in_browser": open_in_browser,
            "strict": strict,
        },
    )

    serve(
        config,
        files,
        output_path,
        serve_config,
    )


################################################################################

if __name__ == "__main__":
    cli()
