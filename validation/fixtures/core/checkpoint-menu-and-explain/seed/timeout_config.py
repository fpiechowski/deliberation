DEFAULT_TIMEOUT_MS = 5000


def build_timeout_config(timeout_ms: int | None = None) -> dict[str, int]:
    """Build the timeout portion of the client configuration."""
    effective_timeout_ms = (
        DEFAULT_TIMEOUT_MS if timeout_ms is None else timeout_ms
    )
    return {"timeout_ms": effective_timeout_ms}
