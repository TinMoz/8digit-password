from lib.config import load_config
from lib.db import RandomNumberStore
from lib.random_digits import DEFAULT_LENGTH, generate_random_digits


def display_all(numbers) -> None:
    if not numbers:
        print("No numbers stored yet.")
        return

    print("All stored numbers (newest first):")
    for number in numbers:
        print(f"- {number}")


def choose_action() -> str:
    while True:
        choice = input("Select action (1: view history, 2: generate new): ").strip()
        if choice in {"1", "2"}:
            return choice
        print("Invalid choice. Please enter 1 or 2.")


def show_history(store: RandomNumberStore) -> None:
    numbers = store.fetch_numbers(limit=5)
    display_all(numbers)


def generate_and_show(store: RandomNumberStore) -> None:
    new_number = generate_random_digits(DEFAULT_LENGTH)
    store.insert_number(new_number)
    print(f"\nCurrent random number: {new_number}")
    print()
    show_history(store)


def main() -> None:
    config = load_config()
    store = RandomNumberStore(config.db_url)
    store.initialize()
    store.prune_excess(max_records=10)

    action = choose_action()
    if action == "1":
        show_history(store)
    else:
        generate_and_show(store)
        store.prune_excess(max_records=10)

    input("\nPress Enter to exit...")


if __name__ == "__main__":
    main()
