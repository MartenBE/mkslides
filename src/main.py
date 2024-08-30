import argparse
import jinja2
import re
import shutil

from pathlib import Path

################################################################################

MD_IMG_REGEX = re.compile(
    r"""
    !                            # Start of the image
    \[.*?\]                      # Alt text
    \((?P<location>.*?)\)        # Image location
    """,
    re.VERBOSE,
)
HTML_IMG_REGEX = re.compile(
    r"""
    <img                       # Start of the image
    .+?                        # Any attributes
    src=                       # src attribute
        (?P<delimiter>['\"])    # Delimiter
        (?P<location>.*?)       # Image location
        (?P=delimiter)          # Delimiter
    """,
    re.VERBOSE,
)

################################################################################


def detect_images(content):
    images = set()

    for m in MD_IMG_REGEX.finditer(content):
        images.add(m.group("location"))

    for m in HTML_IMG_REGEX.finditer(content):
        images.add(m.group("location"))

    print(images)


def process_md_file(file):
    print(f'Processing "{file}"')
    with open(file, "r") as f:
        markdown_content = f.read()

        # Copy the markdown content to template

        # Copy images

        images = detect_images(markdown_content)


################################################################################


parser = argparse.ArgumentParser(description="reveal-py")
parser.add_argument(
    "files",
    metavar="FILE(S)/DIR",
    type=str,
    help="Path to the markdown file(s), or the directory containing markdown files",
)
parser.add_argument(
    "-o", "--output", type=str, help="Path to the output directory", default="html"
)
parser.add_argument(
    "-c", "--config", type=str, help="Path to the config file", default=".revealpy.yml"
)
args = parser.parse_args()


output_path = Path(args.output)
print(f"Output path: {output_path}")
if output_path.exists():
    print("Output path exists. Deleting and recreating ...")
    shutil.rmtree(output_path)
output_path.mkdir()
shutil.copytree("assets/templates/revealjs", output_path / "assets/revealjs")


environment = jinja2.Environment()
environment.loader = jinja2.FileSystemLoader("assets/templates")
slideshow_template = environment.get_template("slideshow.html")
# index_template = environment.get_template("index.html")

# input_path = Path(args.files)
# for md_file in input_path.glob("**/*.md"):
#     process_md_file(md_file)
