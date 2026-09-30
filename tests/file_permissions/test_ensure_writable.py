# SPDX-FileCopyrightText: Copyright (C) 2026 Johannes Bornhold and Contributors to the project (https://github.com/MartenBE/mkslides/graphs/contributors)
#
# SPDX-License-Identifier: MIT

import shutil
from collections.abc import Generator
from pathlib import Path

import pytest

from mkslides.utils import ensure_writable
from tests.utils import SKIP_UNLESS_POSIX_PERMISSIONS, read_only

pytestmark = SKIP_UNLESS_POSIX_PERMISSIONS


@pytest.fixture
def read_only_tree(tmp_path: Path) -> Generator[Path]:
    """Build a directory tree without its write bit, as a read-only store has."""
    source = tmp_path / "source"
    (source / "themes").mkdir(parents=True)
    (source / "themes" / "theme.css").write_text("body {}")

    with read_only(source) as read_only_source:
        yield read_only_source


def test_copied_tree_can_be_removed_again(
    read_only_tree: Path,
    tmp_path: Path,
) -> None:
    destination = tmp_path / "destination"
    shutil.copytree(read_only_tree, destination)

    ensure_writable(destination)

    shutil.rmtree(destination)
    assert not destination.exists()


def test_copied_file_can_be_overwritten(read_only_tree: Path, tmp_path: Path) -> None:
    destination = tmp_path / "theme.css"
    shutil.copy(read_only_tree / "themes" / "theme.css", destination)
    new_css = "body { color: red; }"
    ensure_writable(destination)

    destination.write_text(new_css)

    assert destination.read_text() == new_css


def test_an_already_writable_tree_keeps_its_mode(tmp_path: Path) -> None:
    source = tmp_path / "source"
    source.mkdir()
    css = source / "theme.css"
    css.write_text("body {}")
    modes_before = (source.stat().st_mode, css.stat().st_mode)

    ensure_writable(source)

    assert (source.stat().st_mode, css.stat().st_mode) == modes_before
