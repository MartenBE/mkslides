import argparse
import jinja2
import re
import shutil

from pathlib import Path

################################################################################

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

################################################################################


def assert_path_exists(path: Path):
    assert path.exists(), f'"{path.absolute()}" does not exist'


################################################################################


parser = argparse.ArgumentParser(description="reveal-py")
parser.add_argument(
    "files",
    metavar="FILE(S)/DIR",
    type=str,
    help="Path to the markdown file(s), or the directory containing markdown files",
)
parser.add_argument(
    "-o", "--output", type=str, help="The output directory", default="html"
)
parser.add_argument(
    "-c", "--config", type=str, help="Path to the config file", default=".revealpy.yml"
)
args = parser.parse_args()

# Input path

input_path = Path(args.files)
print(f'Input path: "{input_path.absolute()}"')
assert_path_exists(input_path)

# Output directory

output_directory = Path(args.output)
print(f'Output directory: "{output_directory.absolute()}"')

if output_directory.exists():
    shutil.rmtree(output_directory)
    print("Output directory already exists: deleted")

output_directory.mkdir()
print(f"Output directory created.")

# Reveal.js

revealjs_path = Path("assets/reveal.js-master")
result_revealjs_path = output_directory / "assets" / "reveal-js"
shutil.copytree(revealjs_path, result_revealjs_path)
print(f'\tCopied "{revealjs_path.absolute()}" to "{result_revealjs_path.absolute()}"')

# Jinja2

environment = jinja2.Environment()
environment.loader = jinja2.FileSystemLoader("assets/templates")
slideshow_template = environment.get_template("slideshow.html.jinja")

# Process markdown files

index = []

for md_file in input_path.glob("**/*.md"):

    # Generate the markup from markdown

    markdown = md_file.read_text()
    result_markup_path = output_directory / md_file.relative_to(input_path)
    result_markup_path = result_markup_path.with_suffix(".html")
    revealjs_path = result_revealjs_path.relative_to(
        result_markup_path.parent, walk_up=True
    )

    markup = slideshow_template.render(
        revealjs_path=revealjs_path,
        markdown=markdown,
    )

    result_markup_path.parent.mkdir(parents=True, exist_ok=True)
    result_markup_path.write_text(markup)
    print(f'Transformed "{md_file.absolute()}" into "{result_markup_path.absolute()}"')

    # Copy images

    for regex in [MD_IMAGE_REGEX, HTML_IMAGE_REGEX, HTML_BACKGROUND_IMAGE_REGEX]:
        for m in regex.finditer(markdown):
            image = Path(md_file.parent, m.group("location"))
            assert_path_exists(image)

            result_image_path = output_directory / image.relative_to(input_path)
            result_image_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(image, result_image_path)
            print(
                f'\t\tCopied "{image.absolute()}" to "{result_image_path.absolute()}"'
            )

    # Index

    index.append(result_markup_path.relative_to(output_directory))

# Generate the index

print(index)
index_template = environment.get_template("index.html.jinja")
index_path = output_directory / "index.html"
index_path.write_text(index_template.render(index=index))
print(f'Generated index: "{index_path.absolute()}"')
