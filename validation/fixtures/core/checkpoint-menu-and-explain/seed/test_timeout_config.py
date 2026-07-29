import unittest

from timeout_config import DEFAULT_TIMEOUT_MS, build_timeout_config


class BuildTimeoutConfigTests(unittest.TestCase):
    def test_uses_default_when_timeout_is_missing(self) -> None:
        self.assertEqual(
            build_timeout_config(),
            {"timeout_ms": DEFAULT_TIMEOUT_MS},
        )

    def test_preserves_explicit_positive_timeout(self) -> None:
        self.assertEqual(
            build_timeout_config(2500),
            {"timeout_ms": 2500},
        )

    def test_preserves_zero_timeout(self) -> None:
        self.assertEqual(
            build_timeout_config(0),
            {"timeout_ms": 0},
        )


if __name__ == "__main__":
    unittest.main()
