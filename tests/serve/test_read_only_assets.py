# SPDX-FileCopyrightText: Copyright (C) 2026 Johannes Bornhold and Contributors to the project (https://github.com/MartenBE/mkslides/graphs/contributors)
#
# SPDX-License-Identifier: MIT

import os
import sys
import threading
from collections.abc import Callable, Generator
from pathlib import Path
from typing import Any

import pytest
from omegaconf import DictConfig, OmegaConf

from mkslides import markupgenerator
from mkslides import serve as serve_module
from mkslides.config import get_config
from tests.utils import read_only

pytestmark = [
    pytest.mark.skipif(
        sys.platform == "win32",
        reason="Relies on POSIX permission bits.",
    ),
    pytest.mark.skipif(
        hasattr(os, "geteuid") and os.geteuid() == 0,
        reason="Root removes read-only directories anyway.",
    ),
]

REBUILD_TIMEOUT_SECONDS = 10


@pytest.fixture
def read_only_assets(tmp_path: Path) -> Generator[Path]:
    """Simulate a read-only reveal.js, the way the Nix store provides one."""
    resource = tmp_path / "reveal.js"
    (resource / "dist").mkdir(parents=True)
    (resource / "dist" / "reveal.js").write_text("// stub\n")

    with read_only(resource) as read_only_resource:
        yield read_only_resource


@pytest.fixture
def talk(tmp_path: Path) -> Path:
    """Give the server a deck to watch."""
    directory = tmp_path / "talk"
    directory.mkdir()
    (directory / "index.md").write_text("# Titel\n\nVORHER\n")
    return directory


def serve_config() -> DictConfig:
    return OmegaConf.structured(
        {
            "debounce_interval": 0.01,
            "dev_ip": "localhost",
            "dev_port": 8000,
            "open_in_browser": False,
            "strict": False,
        },
    )


def serve_and_save(
    talk: Path,
    output_path: Path,
    read_only_assets: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> dict[str, Any]:
    """Serve the talk, save it while the server runs, and report what happened."""
    seen: dict[str, Any] = {"builds": 0, "crashes": [], "shutdown_error": None}
    rebuilt = threading.Event()
    real_build = serve_module.build

    def counting_build(*args: Any, **kwargs: Any) -> None:
        seen["builds"] += 1
        try:
            real_build(*args, **kwargs)
        finally:
            if seen["builds"] > 1:
                rebuilt.set()

    class FakeServer:
        def __init__(self) -> None:
            self.watches: list[tuple[str, Callable[[], None]]] = []

        def watch(self, filepath: str, func: Callable[[], None]) -> None:
            self.watches.append((filepath, func))

        def serve(self, **_kwargs: Any) -> None:
            (talk / "index.md").write_text("# Titel\n\nNACHHER\n")
            for _filepath, func in self.watches:
                func()
            rebuilt.wait(REBUILD_TIMEOUT_SECONDS)

    monkeypatch.setattr(markupgenerator, "REVEALJS_RESOURCE", read_only_assets)
    monkeypatch.setattr(serve_module, "build", counting_build)
    monkeypatch.setattr(serve_module.livereload, "Server", FakeServer)
    monkeypatch.setattr(
        threading,
        "excepthook",
        lambda args: seen["crashes"].append(args.exc_value),
    )

    try:
        serve_module.serve(get_config(None), talk, output_path, serve_config())
    except OSError as error:
        seen["shutdown_error"] = error

    return seen


def test_saving_a_slide_rebuilds_over_read_only_assets(
    read_only_assets: Path,
    talk: Path,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    output_path = tmp_path / "out"

    seen = serve_and_save(talk, output_path, read_only_assets, monkeypatch)

    builds_at_startup = 1
    assert seen["builds"] == builds_at_startup + 1, "the save triggered no rebuild"
    assert seen["crashes"] == [], "the rebuild printed a traceback"
    assert seen["shutdown_error"] is None, "the server could not remove its output"
    assert not output_path.exists()
