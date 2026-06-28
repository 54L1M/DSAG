"""Reference solution — linear search."""

from __future__ import annotations


def linear_search(arr: list[int], target: int) -> int:
    for i, value in enumerate(arr):
        if value == target:
            return i
    return -1
