import random


def connect(lanes_t: list[list], start: int=0, end: int=1) -> list[int]:
    x = random.randint(start, len(lanes_t) - end)
    y = random.randint(0, len(lanes_t[x]) - 1)
    return [x, y]
