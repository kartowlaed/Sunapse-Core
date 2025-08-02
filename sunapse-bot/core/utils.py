import random


def render_bar(value, max_value, length=10, symbol='\u2588', empty='-'):
    """Return a progress bar using ``symbol`` for filled and ``empty`` for the rest."""
    if max_value <= 0:
        max_value = 1
    filled = int(max(0, min(value, max_value)) / max_value * length)
    return symbol * filled + empty * (length - filled)


def dice(low, high):
    return random.randint(low, high)
