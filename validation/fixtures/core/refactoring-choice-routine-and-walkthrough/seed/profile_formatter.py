def render_profile(record: dict[str, str]) -> str:
    name = record.get("name", "").strip()
    email = record.get("email", "").strip().lower()

    if not name:
        raise ValueError("name is required")
    if email and ("@" not in email or email.startswith("@") or email.endswith("@")):
        raise ValueError("email is invalid")

    if email:
        return f"{name} <{email}>"
    return name
