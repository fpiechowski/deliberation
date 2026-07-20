def authorize_request(
    headers: dict[str, str],
    required_scope: str,
    sessions: dict[str, dict[str, object]],
) -> int:
    credential = headers.get("Authorization", "")

    if credential.startswith("Bearer "):
        token = credential.removeprefix("Bearer ")
    else:
        token = credential

    session = sessions.get(token)
    if session is None or session.get("revoked", False):
        return 401

    scopes = session.get("scopes", ())
    if required_scope not in scopes:
        return 403

    return 200
