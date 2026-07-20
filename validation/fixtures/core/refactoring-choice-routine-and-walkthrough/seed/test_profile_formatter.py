import unittest

from profile_formatter import render_profile


class RenderProfileTests(unittest.TestCase):
    def test_normalizes_and_renders_name_with_email(self) -> None:
        self.assertEqual(
            render_profile({"name": "  Ada Lovelace ", "email": " ADA@EXAMPLE.COM "}),
            "Ada Lovelace <ada@example.com>",
        )

    def test_renders_name_without_email(self) -> None:
        self.assertEqual(render_profile({"name": "Grace Hopper"}), "Grace Hopper")

    def test_requires_name(self) -> None:
        with self.assertRaisesRegex(ValueError, "name is required"):
            render_profile({"name": "  ", "email": "ada@example.com"})

    def test_rejects_invalid_email(self) -> None:
        with self.assertRaisesRegex(ValueError, "email is invalid"):
            render_profile({"name": "Ada", "email": "invalid"})

    def test_input_is_not_mutated(self) -> None:
        record = {"name": "  Ada ", "email": " ADA@EXAMPLE.COM "}
        expected = dict(record)

        render_profile(record)

        self.assertEqual(record, expected)


if __name__ == "__main__":
    unittest.main()
