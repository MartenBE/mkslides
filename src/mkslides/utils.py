# SPDX-FileCopyrightText: Copyright (C) 2024 Martijn Saelens and Contributors to the project (https://github.com/MartenBE/mkslides/graphs/contributors)
#
# SPDX-License-Identifier: MIT

from pathlib import Path
from urllib.parse import urlparse

from mkslides.constants import DESTINATION_DIR_MODE, DESTINATION_FILE_MODE
from mkslides.urltype import URLType


def parse_ip_port(
    ip_port_str: str,
) -> tuple[str, int]:
    urlparse_result = urlparse(f"//{ip_port_str}")
    ip = urlparse_result.hostname
    port = urlparse_result.port

    assert ip, f"Invalid IP address: {ip_port_str}"
    assert port, f"Invalid port: {ip_port_str}"

    return ip, port


def normalize_permissions(path: Path) -> None:
    if not path.is_dir():
        path.chmod(DESTINATION_FILE_MODE)
        return

    path.chmod(DESTINATION_DIR_MODE)

    for root, dirs, files in path.walk():
        for name in dirs:
            (root / name).chmod(DESTINATION_DIR_MODE)
        for name in files:
            file = root / name
            if not file.is_symlink():
                file.chmod(DESTINATION_FILE_MODE)


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
