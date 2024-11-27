#!/usr/bin/env python3

import re
import subprocess
from pathlib import Path

################################################################################

files = ["README.md", "docs/index.md"]
no_command_start = "<!-- output-no-command -->"
no_command_end = "<!-- /output-no-command -->"
build_start = "<!-- output-build -->"
build_end = "<!-- /output-build -->"
serve_start = "<!-- output-serve -->"
serve_end = "<!-- /output-serve -->"

################################################################################


def replace_content(
    content: str, start_marker: str, end_marker: str, new_content: str,
) -> str:
    pattern = f"{start_marker}.*?{end_marker}"
    replacement = f"{start_marker}\n```text\n{new_content}\n```\n{end_marker}"
    return re.sub(pattern, replacement, content, flags=re.DOTALL)


################################################################################

no_command_output = subprocess.check_output(
    ["poetry", "run", "mkslides", "-h"],
    universal_newlines=True,
)

build_output = subprocess.check_output(
    ["poetry", "run", "mkslides", "build", "-h"],
    universal_newlines=True,
)
serve_output = subprocess.check_output(
    ["poetry", "run", "mkslides", "serve", "-h"],
    universal_newlines=True,
)

for file_path in files:
    file = Path(file_path)

    content = file.read_text()
    content = replace_content(
        content,
        no_command_start,
        no_command_end,
        no_command_output,
    )
    content = replace_content(content, build_start, build_end, build_output)
    content = replace_content(content, serve_start, serve_end, serve_output)

    file.write_text(content)

    print(f"Updated {file}")
