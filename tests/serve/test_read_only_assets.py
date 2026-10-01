# SPDX-FileCopyrightText: Copyright (C) 2026 Johannes Bornhold and Contributors to the project (https://github.com/MartenBE/mkslides/graphs/contributors)
#
# SPDX-License-Identifier: MIT

import os
import signal
import socket
import subprocess
import time
from collections.abc import Callable, Generator
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path

from tests.utils import SKIP_UNLESS_POSIX_PERMISSIONS

pytestmark = SKIP_UNLESS_POSIX_PERMISSIONS

BEFORE = "BEFORE"
AFTER = "AFTER"
WAIT_SECONDS = 15.0
POLL_SECONDS = 0.05


def free_port() -> int:
    with socket.socket() as sock:
        sock.bind(("localhost", 0))
        return int(sock.getsockname()[1])


def is_listening(port: int) -> bool:
    with socket.socket() as sock:
        sock.settimeout(POLL_SECONDS)
        return sock.connect_ex(("localhost", port)) == 0


def read_when_rebuilt(rendered: Path) -> str:
    """Return the rendered deck, or an empty string until it shows the new text."""
    try:
        html = rendered.read_text()
    except OSError:
        return ""
    return html if AFTER in html else ""


@dataclass(frozen=True)
class DevServer:
    process: "subprocess.Popen[str]"
    log_path: Path
    port: int

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

    def wait_until_ready(self) -> None:
        """Wait until the port is open, which is after the watcher has started."""
        self.wait_for(
            lambda: "listening" if is_listening(self.port) else "",
            "the server start listening",
        )

    def interrupt(self) -> int:
        self.process.send_signal(signal.SIGINT)
        return self.process.wait(timeout=WAIT_SECONDS)


@contextmanager
def serving(
    talk: Path,
    read_only_install: Path,
    server_tmp: Path,
    log_path: Path,
) -> Generator[DevServer]:
    """Run a development server on the talk, out of the read-only install."""
    port = free_port()
    with log_path.open("w") as log:
        process = subprocess.Popen(
            [
                "mkslides",
                "serve",
                "--debounce-interval",
                "0.1",
                "-a",
                f"localhost:{port}",
                str(talk),
            ],
            env={
                **os.environ,
                "PYTHONPATH": str(read_only_install),
                "TMPDIR": str(server_tmp),
            },
            stdout=log,
            stderr=subprocess.STDOUT,
            text=True,
        )
        try:
            yield DevServer(process, log_path, port)
        finally:
            if process.poll() is None:
                process.kill()


def test_a_read_only_install_serves_rebuilds_and_cleans_up(
    read_only_install: Path,
    tmp_path: Path,
) -> None:
    talk = tmp_path / "talk"
    server_tmp = tmp_path / "tmp"
    talk.mkdir()
    server_tmp.mkdir()
    slide = talk / "index.md"
    slide.write_text(f"# Title\n\n{BEFORE}\n")
    log_path = tmp_path / "serve.log"

    with serving(talk, read_only_install, server_tmp, log_path) as server:
        server.wait_until_ready()
        output_path = next(server_tmp.glob("mkslides_*"))

        slide.write_text(f"# Title\n\n{AFTER}\n")

        rendered = server.wait_for(
            lambda: read_when_rebuilt(output_path / "index.html"),
            "the saved slide in the rebuilt deck",
        )
        returncode = server.interrupt()

    assert AFTER in rendered
    assert BEFORE not in rendered
    assert "Traceback" not in log_path.read_text(), "the server printed a traceback"
    assert returncode == 0
    assert not output_path.exists(), "the server left its output behind"
