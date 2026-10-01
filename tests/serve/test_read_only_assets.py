# SPDX-FileCopyrightText: Copyright (C) 2026 Johannes Bornhold and Contributors to the project (https://github.com/MartenBE/mkslides/graphs/contributors)
#
# SPDX-License-Identifier: MIT

import os
import signal
import socket
import subprocess
import time
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import IO

import pytest

from tests.utils import SKIP_UNLESS_POSIX_PERMISSIONS

pytestmark = SKIP_UNLESS_POSIX_PERMISSIONS

BEFORE = "BEFORE"
AFTER = "AFTER"
WAIT_SECONDS = 15.0
POLL_SECONDS = 0.05


@dataclass(frozen=True)
class ServeSession:
    """The result of one serve run."""

    rendered: str
    log: str
    returncode: int
    output_removed: bool


@dataclass(frozen=True)
class RunningServer:
    process: "subprocess.Popen[str]"
    log_path: Path

    def wait_for(self, produce: Callable[[], str], what: str) -> str:
        deadline = time.monotonic() + WAIT_SECONDS
        while time.monotonic() < deadline:
            produced = produce()
            if produced:
                return produced
            if self.process.poll() is not None:
                break
            time.sleep(POLL_SECONDS)

        message = f"never saw {what}\n\nServer log:\n{self.log_path.read_text()}"
        raise AssertionError(message)


def free_port() -> int:
    with socket.socket() as sock:
        sock.bind(("localhost", 0))
        return int(sock.getsockname()[1])


def read_when_rebuilt(rendered: Path) -> str:
    """Return the rendered deck, or an empty string until it shows the new text."""
    try:
        html = rendered.read_text()
    except OSError:
        return ""
    return html if AFTER in html else ""


def start_server(
    talk: Path,
    read_only_install: Path,
    server_tmp: Path,
    log: IO[str],
) -> "subprocess.Popen[str]":
    command = [
        "mkslides",
        "-v",
        "serve",
        "--debounce-interval",
        "0.1",
        "-a",
        f"localhost:{free_port()}",
        str(talk),
    ]
    return subprocess.Popen(
        command,
        env={
            **os.environ,
            "PYTHONPATH": str(read_only_install),
            "TMPDIR": str(server_tmp),
        },
        stdout=log,
        stderr=subprocess.STDOUT,
        text=True,
    )


@pytest.fixture(scope="module")
def serve_session(
    read_only_install: Path,
    tmp_path_factory: pytest.TempPathFactory,
) -> ServeSession:
    """Serve the talk, save a slide, then interrupt the server."""
    root = tmp_path_factory.mktemp("serve")
    server_tmp = root / "tmp"
    talk = root / "talk"
    server_tmp.mkdir()
    talk.mkdir()
    slide = talk / "index.md"
    slide.write_text(f"# Title\n\n{BEFORE}\n")
    log_path = root / "serve.log"

    with log_path.open("w") as log:
        server = RunningServer(
            start_server(talk, read_only_install, server_tmp, log),
            log_path,
        )
        try:
            output_path = Path(
                server.wait_for(
                    lambda: next(
                        (str(path) for path in server_tmp.glob("mkslides_*")),
                        "",
                    ),
                    "an output directory",
                ),
            )
            rendered_path = output_path / "index.html"
            server.wait_for(
                lambda: str(rendered_path) if rendered_path.exists() else "",
                "the initial build",
            )

            slide.write_text(f"# Title\n\n{AFTER}\n")
            rendered = server.wait_for(
                lambda: read_when_rebuilt(rendered_path),
                "the saved slide in the rebuilt deck",
            )

            server.process.send_signal(signal.SIGINT)
            returncode = server.process.wait(timeout=WAIT_SECONDS)
        finally:
            if server.process.poll() is None:
                server.process.kill()

    return ServeSession(
        rendered=rendered,
        log=log_path.read_text(),
        returncode=returncode,
        output_removed=not output_path.exists(),
    )


def test_saving_a_slide_rebuilds_the_deck(serve_session: ServeSession) -> None:
    assert AFTER in serve_session.rendered
    assert BEFORE not in serve_session.rendered
    assert "Traceback" not in serve_session.log, "the server printed a traceback"


def test_interrupting_the_server_removes_its_output(
    serve_session: ServeSession,
) -> None:
    assert serve_session.returncode == 0
    assert serve_session.output_removed, "the server left its output behind"
