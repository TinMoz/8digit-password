import sys
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from lib.db import RandomNumberStore


class RandomNumberStoreTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = TemporaryDirectory(ignore_cleanup_errors=True)
        db_path = Path(self.temp_dir.name) / "test_numbers.db"
        self.store = RandomNumberStore(f"sqlite:///{db_path}")
        self.store.initialize()

    def tearDown(self):
        self.store = None
        self.temp_dir.cleanup()

    def test_should_fetch_newest_first(self):
        numbers = ["00000001", "12345678", "99999999"]
        for number in numbers:
            self.store.insert_number(number)

        fetched = self.store.fetch_numbers()
        self.assertEqual(list(reversed(numbers)), fetched)

    def test_should_limit_results(self):
        for index in range(5):
            self.store.insert_number(f"{index:08d}")

        limited = self.store.fetch_numbers(limit=2)
        self.assertEqual(2, len(limited))
        self.assertEqual(["00000004", "00000003"], limited)

    def test_should_hide_after_marked_viewed(self):
        self.store.insert_number("11111111")
        latest = self.store.fetch_latest_unseen()
        self.assertIsNotNone(latest)

        record_id, value = latest
        self.assertEqual("11111111", value)
        self.store.mark_viewed(record_id)

        none_left = self.store.fetch_latest_unseen()
        self.assertIsNone(none_left)

    def test_should_prune_to_max_records(self):
        for index in range(12):
            self.store.insert_number(f"{index:08d}")

        self.store.prune_excess(max_records=10)

        remaining = self.store.fetch_numbers()
        self.assertEqual(10, len(remaining))
        self.assertEqual("00000011", remaining[0])
        self.assertEqual("00000002", remaining[-1])


if __name__ == "__main__":
    unittest.main()
