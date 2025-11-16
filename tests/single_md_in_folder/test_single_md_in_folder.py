# SPDX-FileCopyrightText: Copyright (C) 2024 Martijn Saelens and Contributors to the project (https://github.com/MartenBE/mkslides/graphs/contributors)
#
# SPDX-License-Identifier: MIT

from typing import Any

from tests.utils import (
    assert_file_does_not_exist,
    assert_file_exist,
    assert_html_contains,
    run_build_strict,
)


def test_single_md_files_in_folder(setup_paths: Any) -> None:
    cwd, output_path = setup_paths
    input_path = cwd / "single_md_in_folder" / "slides"
    run_build_strict(cwd, input_path, output_path, None)

    assert_file_exist(output_path / "index.html")
    assert_html_contains(output_path / "index.html", "Lorem ipsum dolor sit amet")

    assert_file_does_not_exist(output_path / "someslides-1.html")
    assert_file_does_not_exist(output_path / "someslides-2.html")


def test_multiple_md_files_in_folder(setup_paths: Any) -> None:
    cwd, output_path = setup_paths
    input_path = cwd / "single_md_in_folder" / "slides-2"
    run_build_strict(cwd, input_path, output_path, None)

    assert_file_exist(output_path / "index.html")
    assert_html_contains(output_path / "index.html", "<h1>Index</h1>")
    assert_file_exist(output_path / "someslides-1.html")
    assert_html_contains(
        output_path / "someslides-1.html",
        "Lorem ipsum dolor sit amet",
    )
    assert_file_exist(output_path / "someslides-2.html")
    assert_html_contains(
        output_path / "someslides-2.html",
        "Lorem ipsum dolor sit amet",
    )
