# SPDX-FileCopyrightText: Copyright (C) 2024 Martijn Saelens and Contributors to the project (https://github.com/MartenBE/mkslides/graphs/contributors)
#
# SPDX-License-Identifier: MIT

import re
from typing import Any

from tests.utils import (
    assert_html_contains,
    assert_html_contains_regexp,
    run_build_strict,
)


# Necessary for livereload to work properly
def test_revealjs_default_options(setup_paths: Any) -> None:
    cwd, output_path = setup_paths
    input_path = cwd / "revealjs_options" / "slides"
    run_build_strict(cwd, input_path, output_path, None)

    assert_html_contains(output_path / "index.html", "history: true,")


def test_revealjs_integer_options(setup_paths: Any) -> None:
    cwd, output_path = setup_paths
    input_path = cwd / "revealjs_options" / "slides"
    config_path = cwd / "revealjs_options" / "revealjs_integer_options-config.yml"
    run_build_strict(cwd, input_path, output_path, config_path)

    assert_html_contains_regexp(
        output_path / "index.html",
        re.compile(
            r"""
            Reveal\.initialize\({
                .*?
                height:\s+1080,
                .*?
                width:\s+1920,
                .*?
            }\);
            """,
            re.VERBOSE | re.DOTALL,
        ),
    )


def test_revealjs_string_options(setup_paths: Any) -> None:
    cwd, output_path = setup_paths
    input_path = cwd / "revealjs_options" / "slides"
    config_path = cwd / "revealjs_options" / "revealjs_string_options-config.yml"
    run_build_strict(cwd, input_path, output_path, config_path)

    assert_html_contains_regexp(
        output_path / "index.html",
        re.compile(
            r"""
            Reveal\.initialize\({
                .*?
                transition:\s+"fade",
                .*?
            }\);
            """,
            re.VERBOSE | re.DOTALL,
        ),
    )
