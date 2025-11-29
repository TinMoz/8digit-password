import time

from lib.config import load_config
from lib.db import RandomNumberStore


def main() -> None:
    config = load_config()
    store = RandomNumberStore(config.db_url)
    store.initialize()

    latest = store.fetch_latest_unseen()
    if not latest:
        print("No numbers found yet. Run A.py first to generate one.")
    else:
        record_id, value = latest
        print(f"Latest random number: {value}")
        store.mark_viewed(record_id)

    for remaining in range(5, 0, -1):
        print(f"Closing in {remaining} seconds...", end="\r")
        time.sleep(1)
    print("Closing in 0 seconds...            ")


if __name__ == "__main__":
    main()
