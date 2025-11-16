# SPDX-FileCopyrightText: Copyright (C) 2024 Martijn Saelens and Contributors to the project (https://github.com/MartenBE/mkslides/graphs/contributors)
#
# SPDX-License-Identifier: MIT

from typing import Any

from tests.utils import assert_html_contains, run_build_strict


def test_text(setup_paths: Any) -> None:
    cwd, output_path = setup_paths
    input_path = cwd / "text" / "slides"
    run_build_strict(cwd, input_path, output_path, None)
    # No exceptions allowed


def test_emojize(setup_paths: Any) -> None:
    cwd, output_path = setup_paths
    input_path = cwd / "text" / "slides"
    run_build_strict(cwd, input_path, output_path, None)

    assert_html_contains(output_path / "someslides-1.html", "⚠️")
    assert_html_contains(output_path / "someslides-1.html", "👍")
