# SPDX-FileCopyrightText: Copyright (C) 2024 Martijn Saelens and Contributors to the project (https://github.com/MartenBE/mkslides/graphs/contributors)
#
# SPDX-License-Identifier: MIT

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
