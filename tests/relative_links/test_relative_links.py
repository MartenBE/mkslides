# SPDX-FileCopyrightText: Copyright (C) 2024 Martijn Saelens and Contributors to the project (https://github.com/MartenBE/mkslides/graphs/contributors)
#
# SPDX-License-Identifier: MIT

import re
import subprocess
from typing import Any

from tests.utils import run_build_strict


def test_existing_relative_links(setup_paths: Any) -> None:
    cwd, output_path = setup_paths
    input_path = cwd / "relative_links" / "slides"
    run_build_strict(cwd, input_path, output_path, None)
    # No exceptions allowed


def test_non_existing_relative_links_without_strict(setup_paths: Any) -> None:
    cwd, output_path = setup_paths
    expected_returncode = 0

    for slides_folder, missing_file in [
        ("slides-non-existing-relative-md-link", "non-existing-file.md"),
        ("slides-non-existing-relative-img-link", "non-existing-file.png"),
        ("slides-non-existing-relative-a-link", "non-existing-file.txt"),
    ]:
        input_path = cwd / "relative_links" / slides_folder
        result = subprocess.run(
            [
                "mkslides",
                "-v",
                "build",
                "-d",
                output_path,
                input_path,
            ],
            cwd=cwd,
            capture_output=True,
            text=True,
            check=False,
        )
        assert result.returncode == expected_returncode
        assert re.search(
            rf"WARNING\s+File\s+'.*someslides-1.md'\s+contains\s+a\s+link\s+'{missing_file}',\s+but\s+the\s+target\s+is\s+not\s+found\s+among\s+slide\s+files.",
            result.stdout,
            flags=re.DOTALL,
        ), result.stdout


def test_non_existing_relative_links_with_strict(setup_paths: Any) -> None:
    cwd, output_path = setup_paths
    expected_returncode = 1

    for slides_folder, missing_file in [
        ("slides-non-existing-relative-md-link", "non-existing-file.md"),
        ("slides-non-existing-relative-img-link", "non-existing-file.png"),
        ("slides-non-existing-relative-a-link", "non-existing-file.txt"),
    ]:
        input_path = cwd / "relative_links" / slides_folder
        result = subprocess.run(
            [
                "mkslides",
                "-v",
                "build",
                "-s",
                "-d",
                output_path,
                input_path,
            ],
            cwd=cwd,
            capture_output=True,
            text=True,
            check=False,
        )
        assert result.returncode == expected_returncode
        assert re.search(
            rf"FileNotFoundError:\s+File\s+'.*someslides-1.md'\s+contains\s+a\s+link\s+'{missing_file}',\s+but\s+the\s+target\s+is\s+not\s+found\s+among\s+slide\s+files.",
            result.stderr,
            flags=re.DOTALL,
        ), result.stderr
