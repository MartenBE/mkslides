# SPDX-FileCopyrightText: Copyright (C) 2024 Martijn Saelens and Contributors to the project (https://github.com/MartenBE/mkslides/graphs/contributors)
#
# SPDX-License-Identifier: MIT

import asyncio
from collections.abc import Callable
from pathlib import Path
from typing import Any

import pytest
from livereload.handlers import LiveReloadHandler  # type: ignore[import-untyped]
from omegaconf import OmegaConf

from mkslides import serve as serve_module
from mkslides.config import get_config


@pytest.fixture
def talk(tmp_path: Path) -> Path:
    directory = tmp_path / "talk"
    directory.mkdir()
    (directory / "index.md").write_text("# Titel\n\nVORHER\n")
    return directory


def serve_and_save(
    talk: Path,
    output_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    saves: int = 1,
) -> dict[str, Any]:
    """Serve the talk, save it while the server runs, and report what happened."""
    seen: dict[str, Any] = {"builds": 0, "announcements": 0}

    real_build = serve_module.build

    def counting_build(*args: Any, **kwargs: Any) -> None:
        seen["builds"] += 1
        real_build(*args, **kwargs)

    def announce() -> None:
        seen["announcements"] += 1
        seen["html_when_announced"] = (output_path / "index.html").read_text()

    class FakeServer:
        def __init__(self) -> None:
            self.watches: list[tuple[str, Callable[[], None], Any]] = []

        def watch(
            self,
            filepath: str,
            func: Callable[[], None],
            delay: Any = None,
        ) -> None:
            self.watches.append((filepath, func, delay))

        def serve(self, **_kwargs: Any) -> None:
            seen["delays"] = [delay for _path, _func, delay in self.watches]
            for _ in range(saves):
                (talk / "index.md").write_text("# Titel\n\nNACHHER\n")
                for _path, func, _delay in self.watches:
                    func()

    monkeypatch.setattr(serve_module.livereload, "Server", FakeServer)
    monkeypatch.setattr(serve_module, "build", counting_build)
    monkeypatch.setattr(LiveReloadHandler, "reload_waiters", announce)

    serve_config = OmegaConf.structured(
        {
            "debounce_interval": 0.01,
            "dev_ip": "localhost",
            "dev_port": 8000,
            "open_in_browser": False,
            "strict": False,
        },
    )

    async def scenario() -> None:
        serve_module.serve(get_config(None), talk, output_path, serve_config)

        current = asyncio.current_task()
        scheduled = [task for task in asyncio.all_tasks() if task is not current]
        await asyncio.gather(*scheduled, return_exceptions=True)

    asyncio.run(scenario())

    return seen


def test_the_deck_is_rebuilt_before_the_browser_is_told(
    talk: Path,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    seen = serve_and_save(talk, tmp_path / "out", monkeypatch)

    assert seen["announcements"] == 1, "the browser was never told to reload"
    assert "NACHHER" in seen["html_when_announced"]
    assert "VORHER" not in seen["html_when_announced"]


def test_livereload_does_not_announce_the_reload_itself(
    talk: Path,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    seen = serve_and_save(talk, tmp_path / "out", monkeypatch)

    assert seen["delays"], "nothing was watched"
    assert all(delay == "forever" for delay in seen["delays"])


def test_a_burst_of_saves_is_one_rebuild_and_one_reload(
    talk: Path,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    seen = serve_and_save(talk, tmp_path / "out", monkeypatch, saves=5)

    builds_at_startup = 1
    assert seen["builds"] == builds_at_startup + 1
    assert seen["announcements"] == 1
