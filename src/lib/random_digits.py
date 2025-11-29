import random

DEFAULT_LENGTH = 8


def generate_random_digits(length: int = DEFAULT_LENGTH) -> str:
    if length <= 0:
        raise ValueError("length must be positive")

    max_value = 10 ** length - 1
    return f"{random.randint(0, max_value):0{length}d}"
