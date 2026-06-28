"""Reference solution — binary search."""

from __future__ import annotations


def binary_search(arr: list[int], target: int) -> int:
    lo, hi = 0, len(arr)  # [lo, hi)
    while lo < hi:
        mid = (lo + hi) // 2
        if arr[mid] == target:
            return mid
        if arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid
    return -1
