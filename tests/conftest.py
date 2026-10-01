# SPDX-FileCopyrightText: Copyright (C) 2024 Martijn Saelens and Contributors to the project (https://github.com/MartenBE/mkslides/graphs/contributors)
#
# SPDX-License-Identifier: MIT

import shutil
import tempfile
from collections.abc import Generator
from pathlib import Path

import pytest

import mkslides
from tests.utils import read_only

PACKAGE_ROOT = Path(mkslides.__file__).parent


@pytest.fixture(scope="module")
def read_only_install(tmp_path_factory: pytest.TempPathFactory) -> Generator[Path]:
    """Simulate a read-only install, like the one in the Nix store."""
    prefix = tmp_path_factory.mktemp("site-packages")
    shutil.copytree(PACKAGE_ROOT, prefix / PACKAGE_ROOT.name)

    with read_only(prefix) as read_only_prefix:
        yield read_only_prefix


@pytest.fixture(scope="module")
def setup_paths() -> Generator[tuple[Path, Path]]:
    cwd = Path("tests").resolve(strict=True)
    output_path = Path(tempfile.mkdtemp(prefix="mkslides_")).resolve(strict=False)

    yield cwd, output_path

    if output_path.exists():
        shutil.rmtree(output_path)
