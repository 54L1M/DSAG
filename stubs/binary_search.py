"""Binary search — halve the search space each step on a sorted list."""

from __future__ import annotations


def binary_search(arr: list[int], target: int) -> int:
    """Return the index of `target` in the **ascending-sorted** `arr`, or -1.

    Keep a [low, high) window. Look at the middle; if it equals the target you
    are done, otherwise discard the half that cannot contain the target.

    Precondition: `arr` is sorted ascending.
    Time: O(log n). Space: O(1).
    """
    raise NotImplementedError  # remove this line and implement
