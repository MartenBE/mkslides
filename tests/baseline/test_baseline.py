# SPDX-FileCopyrightText: Copyright (C) 2024 Martijn Saelens and Contributors to the project (https://github.com/MartenBE/mkslides/graphs/contributors)
#
# SPDX-License-Identifier: MIT

import stat
from pathlib import Path
from typing import Any

import pytest

from tests.utils import (
    assert_file_exist,
    assert_file_user_writable,
    assert_html_contains,
    run_build_strict,
)


# Git does not track write permissions, so remove them before the test.
#
@pytest.fixture
def remove_user_write_permission() -> None:
    folder_path = Path("tests/baseline/slides/no-write-permission").resolve(strict=True)
    files = [
        folder_path / "no-write-permission.md",
        folder_path / "no-write-permission-asset.txt",
    ]

    for file in files:
        file.chmod(file.stat().st_mode & ~stat.S_IWUSR)


@pytest.mark.usefixtures("remove_user_write_permission")
def test_process_directory_without_config(setup_paths: Any) -> None:
    cwd, output_path = setup_paths
    input_path = cwd / "baseline" / "slides"
    run_build_strict(cwd, input_path, output_path, None)

    assert_file_exist(output_path / "mkslides-assets/reveal-js/dist/reveal.css")
    assert_file_exist(output_path / "mkslides-assets/reveal-js/dist/reveal.js")
    assert_file_exist(
        output_path / "mkslides-assets/reveal-js/dist/plugin/markdown.js",
    )
    assert_file_exist(
        output_path / "mkslides-assets/reveal-js/dist/plugin/highlight.js",
    )
    assert_file_exist(output_path / "mkslides-assets/reveal-js/dist/plugin/zoom.js")
    assert_file_exist(output_path / "mkslides-assets/reveal-js/dist/theme/black.css")
    assert_file_exist(output_path / "mkslides-assets/highlight-js-themes/monokai.css")

    assert_file_exist(output_path / "index.html")
    assert_file_exist(output_path / "someslides-1.html")
    assert_file_exist(output_path / "somefolder/someslides-2.html")

    assert_file_exist(output_path / "randomfile-1.txt")
    assert_file_exist(output_path / "somefolder/randomfile-2.txt")
    assert_file_exist(output_path / "extra/randomfile-3.txt")

    file_path = output_path / "no-write-permission/no-write-permission.html"
    assert_file_exist(file_path)
    assert_file_user_writable(file_path)
    file_path = output_path / "no-write-permission/no-write-permission-asset.txt"
    assert_file_exist(file_path)
    assert_file_user_writable(file_path)

    assert_html_contains(
        output_path / "someslides-1.html",
        '<link rel="stylesheet" href="mkslides-assets/reveal-js/dist/reveal.css" />',
    )
    assert_html_contains(
        output_path / "someslides-1.html",
        '<link rel="stylesheet" href="mkslides-assets/reveal-js/dist/theme/black.css" />',
    )
    assert_html_contains(
        output_path / "someslides-1.html",
        '<link rel="stylesheet" href="mkslides-assets/highlight-js-themes/monokai.css" />',
    )

    assert_html_contains(
        output_path / "somefolder" / "someslides-2.html",
        '<link rel="stylesheet" href="../mkslides-assets/reveal-js/dist/reveal.css" />',
    )
    assert_html_contains(
        output_path / "somefolder" / "someslides-2.html",
        '<link rel="stylesheet" href="../mkslides-assets/reveal-js/dist/theme/black.css" />',
    )
    assert_html_contains(
        output_path / "somefolder" / "someslides-2.html",
        '<link rel="stylesheet" href="../mkslides-assets/highlight-js-themes/monokai.css" />',
    )
