# SPDX-FileCopyrightText: Copyright (C) 2026 Martijn Saelens and Contributors to the project (https://github.com/MartenBE/mkslides/graphs/contributors)
#
# SPDX-License-Identifier: MIT

from typing import Any

from tests.utils import assert_html_contains, run_build_strict


def test_default_slide_title(setup_paths: Any) -> None:
    cwd, output_path = setup_paths
    input_path = cwd / "title" / "slides"
    run_build_strict(cwd, input_path, output_path, None)

    assert_html_contains(
        output_path / "someslides-1.html",
        "<title>Slides</title>",
    )

    assert_html_contains(
        output_path / "someslides-2.html",
        "<title>A single slide with a title</title>",
    )


def test_custom_slide_title(setup_paths: Any) -> None:
    cwd, output_path = setup_paths
    input_path = cwd / "title" / "slides"
    config_path = cwd / "title" / "slide-title-config.yml"
    run_build_strict(cwd, input_path, output_path, config_path)

    assert_html_contains(
        output_path / "someslides-1.html",
        "<title>A title for all the slides</title>",
    )

    assert_html_contains(
        output_path / "someslides-2.html",
        "<title>A single slide with a title</title>",
    )
