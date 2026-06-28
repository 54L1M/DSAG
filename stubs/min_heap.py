"""MinHeap — a binary heap that always pops the smallest value."""

from __future__ import annotations


class MinHeap:
    """An array-backed binary min-heap (don't use Python's heapq).

    Store the complete binary tree in a flat list. For the node at index `i`:
      * parent  = (i - 1) // 2
      * left    = 2 * i + 1
      * right   = 2 * i + 2

    insert: append, then "bubble up" while smaller than the parent.
    delete: take index 0 (the min), move the last element to the front, then
    "bubble down" while larger than its smaller child.
    """

    def __init__(self) -> None:
        self.length: int = 0
        # Suggested: self.data = []
        raise NotImplementedError  # remove this line and implement

    def insert(self, value: int) -> None:
        """Add `value` to the heap. O(log n)."""
        raise NotImplementedError

    def delete(self) -> int | None:
        """Remove and return the smallest value, or None if empty. O(log n)."""
        raise NotImplementedError
