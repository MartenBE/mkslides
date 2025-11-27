# SPDX-FileCopyrightText: Copyright (C) 2024 Martijn Saelens and Contributors to the project (https://github.com/MartenBE/mkslides/graphs/contributors)
#
# SPDX-License-Identifier: MIT

from typing import Any

from tests.utils import (
    assert_html_contains,
    assert_html_does_not_contain,
    run_build_strict,
)


def test_index_title(setup_paths: Any) -> None:
    cwd, output_path = setup_paths
    input_path = cwd / "index" / "slides"
    config_path = cwd / "index" / "index_title-config.yml"
    run_build_strict(cwd, input_path, output_path, config_path)

    assert_html_contains(output_path / "index.html", "<title>Lorem ipsum</title>")
    assert_html_contains(
        output_path / "index.html",
        "<h1>Lorem ipsum</h1>",
    )


def test_index_banner(setup_paths: Any) -> None:
    cwd, output_path = setup_paths
    input_path = cwd / "index" / "slides"
    run_build_strict(cwd, input_path, output_path, None)

    assert_html_contains(
        output_path / "index.html",
        'Documentation built with <a href="https://martenbe.github.io/mkslides/" target="_blank">MkSlides</a>.',
    )


def test_index_no_banner(setup_paths: Any) -> None:
    cwd, output_path = setup_paths
    input_path = cwd / "index" / "slides"
    config_path = cwd / "index" / "index_no_banner-config.yml"
    run_build_strict(cwd, input_path, output_path, config_path)

    assert_html_does_not_contain(
        output_path / "index.html",
        'Documentation built with <a href="https://martenbe.github.io/mkslides/" target="_blank">MkSlides</a>.',
    )
