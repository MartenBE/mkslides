import argparse
import jinja2
import json
import livereload
import shutil
import yaml

from pathlib import Path

from markupgenerator import MarkupGenerator

################################################################################


def create_output_directory(
    output_directory: Path, revealjs_path: Path, output_revealjs_path: Path
) -> None:
    if output_directory.exists():
        shutil.rmtree(output_directory)
        print("Output directory already exists: deleted")

    output_directory.mkdir()
    print(f"Output directory created.")

    shutil.copytree(revealjs_path, output_revealjs_path)
    print(
        f'\tCopied "{revealjs_path.absolute()}" to "{output_revealjs_path.absolute()}"'
    )


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

# Configuring paths

input_path = Path(args.files).resolve(strict=True)
print(f'Input path: "{input_path.absolute()}"')

output_directory = Path(args.output).resolve(strict=True)
print(f'Output directory: "{output_directory.absolute()}"')

assets_path = Path("assets").resolve(strict=True)
output_assets_path = output_directory / "assets"

revealjs_path = assets_path / "reveal.js-master"
output_revealjs_path = output_assets_path / "reveal-js"

# Reading configuration

config_path = Path(args.config).resolve()

config = None
if config_path.exists():
    print(f'Config path: "{config_path.absolute()}"')
    with config_path.open() as f:
        config = yaml.safe_load(f)
else:
    print(f'Config path: "{config_path.absolute()}" does not exist, using default values')

print(json.dumps(config, indent=4))

# Configuring templates

environment = jinja2.Environment()
environment.loader = jinja2.FileSystemLoader(assets_path / "templates")

# Process markdown files

mg = MarkupGenerator(environment, input_path, output_directory, output_revealjs_path)

create_output_directory(output_directory, revealjs_path, output_revealjs_path)
mg.create_markup()

# Livereload if requested

if args.watch:

    def reload():
        print("Reloading...")

        create_output_directory(output_directory, revealjs_path, output_revealjs_path)
        mg.create_markup()

    server = livereload.Server()
    server.watch(filepath=input_path, func=reload, delay=1)
    server.serve(root=output_directory)
