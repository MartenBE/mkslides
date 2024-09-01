import argparse
import jinja2
import livereload
import logging

from pathlib import Path

from config import Config
from copier import Copier
from markupgenerator import MarkupGenerator
from rich.logging import RichHandler


################################################################################

# https://realpython.com/python-logging/
logger = logging.getLogger()
logger.setLevel("DEBUG")
# formatter = logging.Formatter(
#     "{asctime} - {levelname} - {message}",
#     style="{",
#     datefmt="%Y-%m-%d %H:%M:%S",
# )

# console_handler = logging.StreamHandler()
# console_handler.setLevel("INFO")
# console_handler.setFormatter(formatter)
# logger.addHandler(console_handler)

logger.addHandler(RichHandler())

################################################################################

parser = argparse.ArgumentParser(description="reveal-py")
parser.add_argument(
    "files",
    metavar="FILE(S)/DIR",
    type=str,
    help="Path to the markdown file(s), or the directory containing markdown files.",
)
parser.add_argument(
    "-c", "--config", type=str, help="Path to the config file.", default=".revealpy.yml"
)
parser.add_argument(
    "-o", "--output", type=str, help="The output directory.", default="html"
)
parser.add_argument(
    "-w",
    "--watch",
    action="store_true",
    help="Watch FILE(S)/DIR and show a preview that automatically reloads on change.",
)

args = parser.parse_args()

################################################################################

# Configuring paths

input_path = Path(args.files).resolve(strict=True)
output_directory = Path(args.output).resolve(strict=True)
copier = Copier(input_path, output_directory)

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

copier.create_output_directory()
markup_generator.create_markup()

# Livereload if requested

if args.watch:

    def reload():
        logger.info("Reloading...")

        copier.create_output_directory()
        markup_generator.create_markup()

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
