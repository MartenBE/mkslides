# SPDX-FileCopyrightText: Copyright (C) 2024 Martijn Saelens and Contributors to the project (https://github.com/MartenBE/mkslides/graphs/contributors)
#
# SPDX-License-Identifier: MIT

from pathlib import Path

import pytest
from click.testing import CliRunner

from mkslides.__main__ import cli


def test_build_without_input_directory_reports_clean_error(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Building without an input dir must report a clean error, not a traceback."""
    monkeypatch.chdir(tmp_path)
    result = CliRunner().invoke(cli, ["build"])
    assert result.exit_code == 1
    assert 'Neither "slides" nor "docs"' in result.output
    assert "Traceback" not in result.output
