"""Quick sort — partition around a pivot, then recurse on each side."""

from __future__ import annotations


def quick_sort(arr: list[int]) -> None:
    """Sort `arr` ascending **in place** (returns None).

    Pick a pivot (a simple choice is the last element). Partition the range so
    everything <= pivot ends up left of it and everything larger ends up right,
    then recurse into the left and right sub-ranges.

    Tip: write a helper `_quick_sort(arr, lo, hi)` and a `_partition` that
    returns the pivot's final index.

    Time: O(n log n) average, O(n^2) worst. Space: O(log n) (recursion).
    """
    raise NotImplementedError  # remove this line and implement
