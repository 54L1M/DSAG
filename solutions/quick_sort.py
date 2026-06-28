"""Reference solution — quick sort (Lomuto partition, in place)."""

from __future__ import annotations


def quick_sort(arr: list[int]) -> None:
    _quick_sort(arr, 0, len(arr) - 1)


def _quick_sort(arr: list[int], lo: int, hi: int) -> None:
    if lo >= hi:
        return
    pivot_idx = _partition(arr, lo, hi)
    _quick_sort(arr, lo, pivot_idx - 1)
    _quick_sort(arr, pivot_idx + 1, hi)


def _partition(arr: list[int], lo: int, hi: int) -> int:
    pivot = arr[hi]
    i = lo  # boundary: arr[lo:i] are all <= pivot
    for j in range(lo, hi):
        if arr[j] <= pivot:
            arr[i], arr[j] = arr[j], arr[i]
            i += 1
    arr[i], arr[hi] = arr[hi], arr[i]
    return i
