"""ArrayList — a dynamic array built on a fixed-capacity backing buffer.

Python's `list` is already a dynamic array, so the lesson here is to implement
the growth strategy yourself: keep a backing buffer with spare capacity and
double it when it fills up. That doubling is what makes `push` *amortized* O(1).
"""

from __future__ import annotations

from typing import Generic, TypeVar

T = TypeVar("T")


class ArrayList(Generic[T]):
    """A growable array.

    Suggested internals: a backing list pre-sized to `capacity` (e.g. filled
    with None) plus a `length` counter. When `length == capacity`, allocate a
    new buffer of double the capacity and copy the elements over.
    """

    def __init__(self, capacity: int = 2) -> None:
        self.length: int = 0
        self.capacity: int = capacity
        raise NotImplementedError  # remove this line and implement

    def get(self, index: int) -> T:
        """Return the item at `index` (IndexError if out of range). O(1)."""
        raise NotImplementedError

    def set(self, index: int, item: T) -> None:
        """Overwrite the item at `index` (IndexError if out of range). O(1)."""
        raise NotImplementedError

    def push(self, item: T) -> None:
        """Append `item` to the end, growing capacity if needed. Amortized O(1)."""
        raise NotImplementedError

    def pop(self) -> T | None:
        """Remove and return the last item, or None if empty. O(1)."""
        raise NotImplementedError

    def insert_at(self, item: T, index: int) -> None:
        """Insert `item` at `index`, shifting later items right. O(n).

        `index == length` appends; `index > length` raises IndexError.
        """
        raise NotImplementedError

    def remove_at(self, index: int) -> T:
        """Remove and return the item at `index`, shifting later items left. O(n)."""
        raise NotImplementedError
