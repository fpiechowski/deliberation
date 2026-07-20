import unittest

from timeout_config import DEFAULT_TIMEOUT_MS, parse_timeout


class ParseTimeoutTests(unittest.TestCase):
    def test_positive_timeout_is_preserved(self) -> None:
        self.assertEqual(parse_timeout("250"), 250)

    def test_zero_currently_falls_back_to_default(self) -> None:
        self.assertEqual(parse_timeout("0"), DEFAULT_TIMEOUT_MS)

    def test_negative_timeout_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "non-negative"):
            parse_timeout("-1")


if __name__ == "__main__":
    unittest.main()
