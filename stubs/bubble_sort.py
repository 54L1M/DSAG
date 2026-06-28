"""Bubble sort — repeatedly swap adjacent out-of-order pairs."""

from __future__ import annotations


def bubble_sort(arr: list[int]) -> None:
    """Sort `arr` ascending **in place** (returns None).

    On each pass, walk the list and swap any adjacent pair that is out of order.
    After pass `i`, the largest `i` items have "bubbled" to the end, so each
    pass can look at one fewer element.

    Time: O(n^2). Space: O(1).
    """
    raise NotImplementedError  # remove this line and implement
