"""Reference solution — two crystal balls."""

from __future__ import annotations

import math


def two_crystal_balls(breaks: list[bool]) -> int:
    n = len(breaks)
    if n == 0:
        return -1
    jump = max(1, int(math.sqrt(n)))

    i = jump
    while i < n:
        if breaks[i]:
            break
        i += jump

    # Walk back to the start of the window and scan linearly.
    i -= jump
    for _ in range(jump + 1):
        if i < n and breaks[i]:
            return i
        i += 1
    return -1
