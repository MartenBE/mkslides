import argparse
import livereload
import logging

from constants import CONFIG_LOCATION, DEFAULT_OUTPUT_DIR
from pathlib import Path

from config import Config
from markupgenerator import MarkupGenerator
from rich.logging import RichHandler


################################################################################

logger = logging.getLogger()
logger.setLevel("DEBUG")
logger.addHandler(RichHandler())

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

    # Reading configuration

    config = Config()
    config_path = Path(args.config).resolve()
    if config_path.exists():
        logger.info(f'Config file found: "{config_path.absolute()}"')
        config.merge_config_from_file(config_path)

    # Configuring paths

    input_path = Path(args.files).resolve(strict=True)

    md_root_path = None
    if input_path.is_dir():
        md_root_path = input_path
    else:
        md_root_path = input_path.parent

    output_directory = Path(args.output).resolve(strict=False)
    markup_generator = MarkupGenerator(config, md_root_path, output_directory)

    # Process markdown files

    markup_generator.create_output_directory()
    markup_generator.process_markdown(input_path)

    # Livereload if requested

    if args.watch:

        def reload():
            logger.info("Reloading...")
            markup_generator.create_output_directory()
            markup_generator.process_markdown(input_path)

        server = livereload.Server()

        paths_to_watch = [input_path]
        for path in [
            config.get("mdslides-reveal", "slides", "theme"),
            config.get("mdslides-reveal", "slides", "template"),
            config.get("mdslides-reveal", "index", "theme"),
            config.get("mdslides-reveal", "index", "template"),
        ]:
            if path:
                paths_to_watch.append(path)

        for path in paths_to_watch:
            server.watch(filepath=path, func=reload)

        server.serve(root=output_directory)

    logger.info("Done")


if __name__ == "__main__":
    main()
