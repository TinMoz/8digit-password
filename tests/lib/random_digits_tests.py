import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from lib.random_digits import DEFAULT_LENGTH, generate_random_digits


class GenerateRandomDigitsTests(unittest.TestCase):
    def test_should_return_eight_digits_by_default(self):
        value = generate_random_digits()
        self.assertEqual(DEFAULT_LENGTH, len(value))
        self.assertTrue(value.isdigit())

    def test_should_allow_custom_length(self):
        value = generate_random_digits(3)
        self.assertEqual(3, len(value))
        self.assertTrue(value.isdigit())

    def test_should_reject_non_positive_length(self):
        with self.assertRaises(ValueError):
            generate_random_digits(0)


if __name__ == "__main__":
    unittest.main()
