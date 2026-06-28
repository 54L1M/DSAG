"""Merge sort — divide in half, sort each half, merge them back."""

from __future__ import annotations


def merge_sort(arr: list[int]) -> list[int]:
    """Return a **new** ascending-sorted list with the same elements as `arr`.

    Split the list in half, recursively sort each half, then merge the two
    sorted halves by repeatedly taking the smaller front element. Stable and
    guaranteed O(n log n), unlike quicksort's worst case.

    Time: O(n log n). Space: O(n).
    """
    raise NotImplementedError  # remove this line and implement
