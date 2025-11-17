# SPDX-FileCopyrightText: Copyright (C) 2024 Martijn Saelens and Contributors to the project (https://github.com/MartenBE/mkslides/graphs/contributors)
#
# SPDX-License-Identifier: MIT

import re
import subprocess
from typing import Any

from tests.utils import (
    assert_html_contains,
    run_build_strict,
)

def test_relative_links_without_strict(setup_paths: Any) -> None:
    cwd, output_path = setup_paths
    expected_returncode = 0

    input_path = cwd / "relative_links" / "slides-fail-1"
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
    # assert re.search(
    #     r"WARNING\s*Relative\s*slideshow\s*link\s*'non-existing-file\.md'\s*in\s*file\s*'.*/someslides-1.md'\s*does\s*not\s*exist",
    #     result.stdout,
    #     flags=re.DOTALL,
    # )

    input_path = cwd / "relative_links" / "slides-fail-2"
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
    # assert re.search(
    #     r"WARNING\s+Relative\s+slideshow\s+link\s+'non-existing-file\.md'\s+in\s+file\s+'.*/someslides-1.md'\s+does\s+not\s+exist",
    #     result.stdout,
    #     flags=re.DOTALL,
    # )


def test_relative_links_with_strict(setup_paths: Any) -> None:
    cwd, output_path = setup_paths
    expected_returncode = 1

    input_path = cwd / "relative_links" / "slides-fail-1"
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
    # assert re.search(
    #     r"FileNotFoundError:\s+Relative\s+slideshow\s+link\s+'non-existing-file\.md'\s+in\s+file\s+'.*/someslides-1\.md'\s+does\s+not\s+exist",
    #     result.stderr,
    # )

    input_path = cwd / "relative_links" / "slides-fail-2"
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
    # assert re.search(
    #     r"FileNotFoundError:\s+Relative\s+slideshow\s+link\s+'non-existing-file\.md'\s+in\s+file\s+'.*/someslides-1\.md'\s+does\s+not\s+exist",
    #     result.stderr,
    # )
