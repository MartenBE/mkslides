#!/usr/bin/env python

import argparse
import importlib
import json
import shutil
import livereload
import logging
import tempfile

from pathlib import Path
from rich.logging import RichHandler
from urllib.parse import urlparse

from .config import Config
from .constants import EXPECTED_CONFIG_LOCATION, DEFAULT_OUTPUT_DIR, REVEALJS_PATH, HIGHLIGHTJS_THEMES_PATH
from .markupgenerator import MarkupGenerator


logger = logging.getLogger()
logger.setLevel("DEBUG")
logger.addHandler(RichHandler(show_path=False))


################################################################################


def main() -> argparse.Namespace:

    # Common arguments

    version = importlib.metadata.version("mkslides-reveal")

    revealjs_version = None
    with (REVEALJS_PATH / "package.json").open() as f:
        revealjs_version = json.load(f)["version"]

    highlightjs_themes_version = None
    with (HIGHLIGHTJS_THEMES_PATH / "package.json").open() as f:
        highlightjs_themes_version = json.load(f)["version"]

    help_argument_data = {
        "action": "help",
        "help": "Show this message and exit.",
    }

    files_argument_data = {
        "metavar": "FILENAME|PATH",
        "help": "Path to the Markdown file, or the directory containing Markdown files.",
    }

    config_file_argument_data = {
        "metavar": "FILENAME",
        "default": EXPECTED_CONFIG_LOCATION,
        "help": "Provide a specific MkSlides-Reveal config file.",
    }

    site_dir_argument_data = {
        "metavar": "PATH",
        "default": DEFAULT_OUTPUT_DIR,
        "help": "The directory to output the result of the slides build.",
    }

    # Global arguments

    parser = argparse.ArgumentParser(
        prog="mkslides-reveal",
        description="MkSlides-Reveal - Slides with Markdown using the power of Reveal.js.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        add_help=False,
    )

    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version=f"MkSlides-Reveal: {version}, Reveal.js version: {revealjs_version}, Highlight.js themes version: {highlightjs_themes_version}",
        help="Show the version and exit.",
    )
    parser.add_argument("-h", "--help", **help_argument_data)

    subparsers = parser.add_subparsers(title="Commands", dest="command")

    # Build arguments

    build_parser = subparsers.add_parser(
        "build",
        help="Build the MkDocs documentation.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        add_help=False,
    )
    build_parser.add_argument("files", **files_argument_data)
    build_parser.add_argument("-f", "--config-file", **config_file_argument_data)
    build_parser.add_argument("-d", "--site-dir", **site_dir_argument_data)
    build_parser.add_argument("-h", "--help", **help_argument_data)
    build_parser.set_defaults(func=build)

    # Serve arguments

    serve_parser = subparsers.add_parser(
        "serve",
        help="Run the builtin development server.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        add_help=False,
    )
    serve_parser.add_argument(
        "files",
        **files_argument_data,
    )
    serve_parser.add_argument(
        "-a",
        "--dev-addr",
        metavar="<IP:PORT>",
        default="localhost:8000",
        help="IP address and port to serve slides locally",
    )
    serve_parser.add_argument(
        "-o",
        "--open",
        action="store_true",
        help="Open the website in a Web browser after the initial build finishes.",
    )
    serve_parser.add_argument(
        "--watch-index-theme",
        action="store_true",
        help="Include the index theme in list of files to watch for live reloading.",
    )
    serve_parser.add_argument(
        "--watch-index-template",
        action="store_true",
        help="Include the index template in list of files to watch for live reloading.",
    )
    serve_parser.add_argument(
        "--watch-slides-theme",
        action="store_true",
        help="Include the slides theme in list of files to watch for live reloading.",
    )
    serve_parser.add_argument(
        "--watch-slides-template",
        action="store_true",
        help="Include the slides template in list of files to watch for live reloading.",
    )
    serve_parser.add_argument("-f", "--config-file", **config_file_argument_data)
    serve_parser.add_argument("-h", "--help", **help_argument_data)
    serve_parser.set_defaults(func=serve)

    # Execute the command

    args = parser.parse_args()

    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


def read_config(config_location: str) -> Config:
    config_path = Path(config_location).resolve()
    config = Config()

    if config_path.exists():
        logger.info(f'Config file found: "{config_path.absolute()}"')
        config.merge_config_from_file(config_path)

    return config


def parse_ip_port(
    ip_port_str: str,
) -> tuple[str, int]:
    urlparse_result = urlparse(f"//{ip_port_str}")
    ip = urlparse_result.hostname
    port = urlparse_result.port

    return ip, port


def build(args):

    logger.info("Command: build")

    # Reading configuration

    config = read_config(args.config_file)

    # Configuring paths

    input_path = Path(args.files).resolve(strict=True)
    md_root_path = input_path if input_path.is_dir() else input_path.parent
    output_directory = Path(args.site_dir).resolve(strict=False)
    markup_generator = MarkupGenerator(config, md_root_path, output_directory)

    # Process markdown files

    markup_generator.create_output_directory()
    markup_generator.process_markdown(input_path)


def serve(args):

    logger.info("Command: serve")

    # Reading configuration

    config = read_config(args.config_file)

    # Configuring paths

    input_path = Path(args.files).resolve(strict=True)
    md_root_path = input_path if input_path.is_dir() else input_path.parent
    site_dir = tempfile.mkdtemp(prefix="mkslides_")
    output_directory = Path(site_dir).resolve(strict=False)
    markup_generator = MarkupGenerator(config, md_root_path, output_directory)

    # Process markdown files

    markup_generator.create_output_directory()
    markup_generator.process_markdown(input_path)

    # Livereload

    def reload():
        logger.info("Reloading...")
        markup_generator.create_output_directory()
        markup_generator.process_markdown(input_path)

    try:
        server = livereload.Server()
        server._setup_logging = (
            lambda: None
        )  # https://github.com/lepture/python-livereload/issues/232

        watched_paths = [
            args.files,
            args.config_file,  # TODO reload config
        ]

        if args.watch_index_theme:
            watched_paths.append(config.get("index", "theme"))
        if args.watch_index_template:
            watched_paths.append(config.get("index", "template"))
        if args.watch_slides_theme:
            watched_paths.append(config.get("slides", "theme"))
        if args.watch_slides_template:
            watched_paths.append(config.get("slides", "template"))

        for path in watched_paths:
            if path:
                path = Path(path).resolve(strict=True)
                logger.info(f'Watching: "{path.absolute()}"')
                server.watch(filepath=path.absolute().as_posix(), func=reload, delay=1)

        ip, port = parse_ip_port(args.dev_addr)

        try:
            server.serve(
                host=ip,
                port=port,
                root=output_directory,
                open_url_delay=0 if args.open else None,
            )
        except KeyboardInterrupt:
            logger.info("Server shut down")

    finally:
        if output_directory.exists():
            shutil.rmtree(output_directory)
            logger.info(f'Removed "{output_directory}"')


if __name__ == "__main__":
    main()
