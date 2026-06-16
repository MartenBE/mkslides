# SPDX-FileCopyrightText: Copyright (C) 2024 Martijn Saelens and Contributors to the project (https://github.com/MartenBE/mkslides/graphs/contributors)
#
# SPDX-License-Identifier: MIT

import os
import stat
from pathlib import Path
from urllib.parse import urlparse

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


def fix_permissions(path: Path):
    for root, dirs, files in os.walk(path):
        for dir in dirs:
            os.chmod(os.path.join(root, dir), stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR)
        for file in files:
            os.chmod(os.path.join(root, file), stat.S_IRUSR | stat.S_IWUSR)
