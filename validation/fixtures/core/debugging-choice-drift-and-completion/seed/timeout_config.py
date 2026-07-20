DEFAULT_TIMEOUT_MS = 5000


def parse_timeout(value: str) -> int:
    """Parse a non-negative timeout in milliseconds."""
    parsed = int(value)
    if parsed < 0:
        raise ValueError("timeout must be non-negative")
    return parsed or DEFAULT_TIMEOUT_MS
