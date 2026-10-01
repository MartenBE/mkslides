# SPDX-FileCopyrightText: Copyright (C) 2024 Martijn Saelens and Contributors to the project (https://github.com/MartenBE/mkslides/graphs/contributors)
#
# SPDX-License-Identifier: MIT

import stat
from pathlib import Path
from urllib.parse import urlparse

from mkslides.urltype import URLType


def ensure_writable(path: Path) -> None:
    """Give the owner write permission on a path and everything below it."""
    entries = [path, *path.rglob("*")] if path.is_dir() else [path]
    for entry in entries:
        mode = stat.S_IMODE(entry.stat().st_mode)
        if not mode & stat.S_IWUSR:
            entry.chmod(mode | stat.S_IWUSR)


def parse_ip_port(
    ip_port_str: str,
) -> tuple[str, int]:
    urlparse_result = urlparse(f"//{ip_port_str}")
    ip = urlparse_result.hostname
    port = urlparse_result.port

    assert ip, f"Invalid IP address: {ip_port_str}"
    assert port, f"Invalid port: {ip_port_str}"

    return ip, port


# TODO: unittests
def get_url_type(url: str) -> URLType:
    if url.startswith("#"):
        return URLType.ANCHOR

    if url.startswith("/"):
        return URLType.ABSOLUTE

    parsed = urlparse(url)
    if parsed.scheme and parsed.scheme != "file":
        return URLType.ABSOLUTE

    p = Path(url)
    if p.is_absolute():
        return URLType.ABSOLUTE

    return URLType.RELATIVE
