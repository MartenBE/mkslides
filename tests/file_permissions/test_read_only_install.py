# SPDX-FileCopyrightText: Copyright (C) 2026 Johannes Bornhold and Contributors to the project (https://github.com/MartenBE/mkslides/graphs/contributors)
#
# SPDX-License-Identifier: MIT

import os
import subprocess
import sys
from pathlib import Path
from typing import Any

from tests.utils import SKIP_UNLESS_POSIX_PERMISSIONS, assert_file_exist, run_build

pytestmark = SKIP_UNLESS_POSIX_PERMISSIONS


def test_read_only_copy_is_imported(read_only_install: Path) -> None:
    result = subprocess.run(
        [sys.executable, "-c", "import mkslides; print(mkslides.__file__)"],
        env={**os.environ, "PYTHONPATH": str(read_only_install)},
        capture_output=True,
        text=True,
        check=True,
    )

    assert result.stdout.strip().startswith(str(read_only_install))


def test_rebuild_succeeds(read_only_install: Path, setup_paths: Any) -> None:
    cwd, output_path = setup_paths
    input_path = cwd / "baseline" / "slides"
    env = {"PYTHONPATH": str(read_only_install)}
    run_build(cwd, input_path, output_path, None, env)

    run_build(cwd, input_path, output_path, None, env)

    assert_file_exist(output_path / "someslides-1.html")
