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


def get_url_type(url: str) -> URLType:
    if url.startswith("#"):
        return URLType.ANCHOR

    if bool(urlparse(url).scheme):
        return URLType.ABSOLUTE

    return URLType.RELATIVE
