"""Two crystal balls — find the breaking floor with only two balls."""

from __future__ import annotations


def two_crystal_balls(breaks: list[bool]) -> int:
    """Return the index of the first `True` in `breaks`, or -1 if none.

    `breaks[i]` is True if a ball dropped from floor `i` breaks. Once it starts
    breaking it never stops (the list is False...False, True...True). You have
    two balls. The trick: jump forward by sqrt(n) with the first ball to find
    the window, then walk that window linearly with the second ball.

    Time: O(sqrt n). Space: O(1).
    """
    raise NotImplementedError  # remove this line and implement
