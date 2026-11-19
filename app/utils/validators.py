import socket
import ipaddress
from urllib.parse import urlparse


def validate_website_url(url: str):

    try:
        parsed = urlparse(url)

        if parsed.scheme not in ["http", "https"]:
            return False

        if not parsed.hostname:
            return False

        if parsed.username or parsed.password:
            return False

        if parsed.port not in [None, 80, 443]:
            return False

        hostname = parsed.hostname

        if hostname.lower() == "localhost":
            return False

        addresses = socket.getaddrinfo(
            hostname,
            None,
            type=socket.SOCK_STREAM
        )

        if not addresses:
            return False

        for address in addresses:

            ip = ipaddress.ip_address(
                address[4][0]
            )

            if not ip.is_global:
                return False

        return True

    except (ValueError, OSError):
        return False