import random


def generate_random_number(x, y):
    """Generate a random number between x and y, inclusive."""
    if isinstance(x, str) or isinstance(y, str):
        return "Provide numbers, not strings."
    return random.randint(x, y)
