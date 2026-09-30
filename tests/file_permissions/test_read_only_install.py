# SPDX-FileCopyrightText: Copyright (C) 2026 Johannes Bornhold and Contributors to the project (https://github.com/MartenBE/mkslides/graphs/contributors)
#
# SPDX-License-Identifier: MIT

import os
import shutil
import subprocess
import sys
from collections.abc import Generator
from pathlib import Path
from typing import Any

import pytest

import mkslides
from tests.utils import (
    SKIP_UNLESS_POSIX_PERMISSIONS,
    assert_file_exist,
    read_only,
    run_build,
)

pytestmark = SKIP_UNLESS_POSIX_PERMISSIONS

PACKAGE_ROOT = Path(mkslides.__file__).parent


@pytest.fixture(scope="module")
def read_only_install(tmp_path_factory: pytest.TempPathFactory) -> Generator[Path]:
    """Simulate a read-only install, the way the Nix store provides one."""
    prefix = tmp_path_factory.mktemp("site-packages")
    shutil.copytree(PACKAGE_ROOT, prefix / PACKAGE_ROOT.name)

    with read_only(prefix) as read_only_prefix:
        yield read_only_prefix


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
