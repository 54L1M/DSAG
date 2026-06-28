"""Insertion sort — grow a sorted prefix one element at a time."""

from __future__ import annotations


def insertion_sort(arr: list[int]) -> None:
    """Sort `arr` ascending **in place** (returns None).

    Treat `arr[:i]` as already sorted. Take `arr[i]` and shift the sorted
    elements that are larger one slot to the right, then drop `arr[i]` into the
    gap. Excellent on nearly-sorted data (close to O(n)).

    Time: O(n^2) worst, O(n) best. Space: O(1).
    """
    raise NotImplementedError  # remove this line and implement
