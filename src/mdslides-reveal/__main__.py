import argparse
import jinja2
import livereload
import logging

from constants import CONFIG_LOCATION, DEFAULT_OUTPUT_DIR
from pathlib import Path

from config import Config
from copier import Copier
from markupgenerator import MarkupGenerator
from rich.logging import RichHandler


################################################################################

logger = logging.getLogger()
logger.setLevel("DEBUG")
logger.addHandler(RichHandler())

################################################################################


################################################################################


def generate_markup(copier: Copier, markup_generator: MarkupGenerator, md_file=None):
    logger.info("Generating markup")

    copier.create_output_directory()

    if md_file:
        markup_generator.process_markdown_file(md_file)
    else:
        markup_generator.process_markdown_directory()


################################################################################


def main():

    # Parsing arguments

    parser = argparse.ArgumentParser(
        description="mdslides-reveal: An easy way to turn Markdown files to HTML slides using the power of Reveal.js."
    )
    parser.add_argument(
        "files",
        metavar="FILE(S)/DIR",
        type=str,
        help="Path to the markdown file(s), or the directory containing markdown files.",
    )
    parser.add_argument(
        "-c",
        "--config",
        type=str,
        help="Path to the config file.",
        default=CONFIG_LOCATION,
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        help="The output directory.",
        default=DEFAULT_OUTPUT_DIR,
    )
    parser.add_argument(
        "-w",
        "--watch",
        action="store_true",
        help="Watch FILE(S)/DIR and show a preview that automatically reloads on change.",
    )

    args = parser.parse_args()

    # Configuring paths

    input_path = Path(args.files).resolve(strict=True)

    md_file = None
    md_root_path = None
    if input_path.is_dir():
        md_root_path = input_path
    else:
        md_file = input_path
        md_root_path = input_path.parent

    output_directory = Path(args.output).resolve(strict=False)
    copier = Copier(md_root_path, output_directory)

    # Reading configuration

    config = Config()
    config_path = Path(args.config).resolve()
    if config_path.exists():
        logger.info(f'Config file found: "{config_path.absolute()}"')
        config.merge_config_from_file(config_path)

    # Configuring templates

    environment = jinja2.Environment()
    environment.loader = jinja2.FileSystemLoader(copier.assets_path / "templates")

    # Process markdown files

    markup_generator = MarkupGenerator(environment, config, copier)

    generate_markup(copier, markup_generator, md_file)

    # Livereload if requested

    if args.watch:

        def reload():
            logger.info("Reloading...")

            generate_markup(copier, markup_generator, md_file)

        server = livereload.Server()

        paths_to_watch = [input_path]
        for path in [
            config.get("reveal-py", "slides", "theme"),
            config.get("reveal-py", "slides", "template"),
            config.get("reveal-py", "index", "theme"),
            config.get("reveal-py", "index", "template"),
        ]:
            if path:
                paths_to_watch.append(path)

        for path in paths_to_watch:
            server.watch(filepath=path, func=reload, delay=1)

        server.serve(root=output_directory)

    logger.info("Done")


if __name__ == "__main__":
    main()
