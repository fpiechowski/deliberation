import unittest

from auth_gateway import authorize_request


class AuthorizeRequestTests(unittest.TestCase):
    def setUp(self) -> None:
        self.sessions = {
            "active-token": {"revoked": False, "scopes": ("read", "write")},
            "limited-token": {"revoked": False, "scopes": ("read",)},
            "revoked-token": {"revoked": True, "scopes": ("read", "write")},
        }

    def test_bearer_token_with_scope_is_authorized(self) -> None:
        self.assertEqual(
            authorize_request(
                {"Authorization": "Bearer active-token"},
                "write",
                self.sessions,
            ),
            200,
        )

    def test_bare_token_is_accepted_for_legacy_compatibility(self) -> None:
        self.assertEqual(
            authorize_request(
                {"Authorization": "active-token"},
                "write",
                self.sessions,
            ),
            200,
        )

    def test_unknown_token_is_unauthorized(self) -> None:
        self.assertEqual(
            authorize_request(
                {"Authorization": "Bearer unknown-token"},
                "read",
                self.sessions,
            ),
            401,
        )

    def test_revoked_token_is_unauthorized(self) -> None:
        self.assertEqual(
            authorize_request(
                {"Authorization": "Bearer revoked-token"},
                "read",
                self.sessions,
            ),
            401,
        )

    def test_missing_scope_is_forbidden(self) -> None:
        self.assertEqual(
            authorize_request(
                {"Authorization": "Bearer limited-token"},
                "write",
                self.sessions,
            ),
            403,
        )


if __name__ == "__main__":
    unittest.main()
