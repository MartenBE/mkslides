import argparse
import livereload
import logging

from constants import (
    EXPECTED_CONFIG_LOCATION,
    DEFAULT_OUTPUT_DIR,
)
from pathlib import Path

from config import Config
from markupgenerator import MarkupGenerator
from rich.logging import RichHandler
from urllib.parse import urlparse

################################################################################

logger = logging.getLogger()
logger.setLevel("DEBUG")
logger.addHandler(RichHandler(show_path=False))


################################################################################


def main() -> argparse.Namespace:

    # Parsing arguments

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
        version="%(prog)s TODO",
        help="Show the version and exit.",
    )
    parser.add_argument(
        "-h", "--help", action="help", help="Show this message and exit."
    )

    subparsers = parser.add_subparsers(title="Commands", dest="command")

    build_parser = subparsers.add_parser(
        "build",
        help="Build the MkDocs documentation.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        add_help=False,
    )
    build_parser.add_argument(
        "files",
        metavar="FILENAME|PATH",
        help="Path to the Markdown file, or the directory containing Markdown files.",
    )
    build_parser.add_argument(
        "-c", "--clean", action="store_true", help="Remove old files before building."
    )
    build_parser.add_argument(
        "-f",
        "--config-file",
        metavar="FILENAME",
        default=EXPECTED_CONFIG_LOCATION,
        help="Provide a specific MkSlides-Reveal config file.",
    )
    build_parser.add_argument(
        "-d",
        "--site-dir",
        metavar="PATH",
        default=DEFAULT_OUTPUT_DIR,
        help="The directory to output the result of the documentation build.",
    )
    build_parser.add_argument(
        "-h", "--help", action="help", help="Show this message and exit."
    )
    build_parser.set_defaults(func=build)

    serve_parser = subparsers.add_parser(
        "serve",
        help="Run the builtin development server.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        add_help=False,
    )
    serve_parser.add_argument(
        "files",
        metavar="FILENAME|PATH",
        help="Path to the Markdown file, or the directory containing Markdown files.",
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
        "--dirty", action="store_true", help="Only re-build files that have changed."
    )
    serve_parser.add_argument(
        "-c", "--clean", action="store_true", help="Remove old files before building."
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
    serve_parser.add_argument(
        "-f",
        "--config-file",
        metavar="FILENAME",
        default=EXPECTED_CONFIG_LOCATION,
        help="Provide a specific MkSlides-Reveal config file.",
    )
    serve_parser.add_argument(
        "-d",
        "--site-dir",
        metavar="PATH",
        default=DEFAULT_OUTPUT_DIR,
        help="The directory to output the result of the documentation build.",
    )
    serve_parser.add_argument(
        "-h", "--help", action="help", help="Show this message and exit."
    )
    serve_parser.set_defaults(func=serve)

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

    if args.clean:
        markup_generator.clear_output_directory()
    markup_generator.create_output_directory()
    markup_generator.process_markdown(input_path)


def serve(args):

    logger.info("Command: serve")

    # Reading configuration

    config = read_config(args.config_file)

    # Configuring paths

    input_path = Path(args.files).resolve(strict=True)
    md_root_path = input_path if input_path.is_dir() else input_path.parent
    output_directory = Path(args.site_dir).resolve(strict=False)
    markup_generator = MarkupGenerator(config, md_root_path, output_directory)

    # Process markdown files

    if args.clean:
        markup_generator.clear_output_directory()
    markup_generator.create_output_directory()
    markup_generator.process_markdown(input_path)

    # Livereload

    def reload():
        logger.info("Reloading...")
        markup_generator.process_markdown(input_path)

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
    server.serve(
        host=ip,
        port=port,
        root=output_directory,
        open_url_delay=0 if args.open else None,
    )

    logger.info("Done")


if __name__ == "__main__":
    main()
