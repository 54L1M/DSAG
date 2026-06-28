"""Singly linked list — nodes chained by a single `next` pointer."""

from __future__ import annotations

from typing import Generic, TypeVar

T = TypeVar("T")


class SinglyLinkedList(Generic[T]):
    """A list backed by singly-linked nodes (head -> ... -> tail -> None).

    Indices are 0-based. Out-of-range indices on get/insert/remove_at should
    raise IndexError. `length` reflects the current number of items.

    All operations are O(1) or O(n) as noted; the point of the exercise is the
    pointer surgery, so implement the nodes yourself (don't wrap a Python list).
    """

    def __init__(self) -> None:
        self.length: int = 0
        # Suggested: self.head and self.tail node references.
        raise NotImplementedError  # remove this line and implement

    def prepend(self, item: T) -> None:
        """Insert `item` at the front. O(1)."""
        raise NotImplementedError

    def append(self, item: T) -> None:
        """Insert `item` at the end. O(1) if you keep a tail pointer."""
        raise NotImplementedError

    def insert_at(self, item: T, index: int) -> None:
        """Insert `item` so it ends up at position `index`. O(n).

        `index == length` appends; `index > length` raises IndexError.
        """
        raise NotImplementedError

    def get(self, index: int) -> T:
        """Return the item at `index` (IndexError if out of range). O(n)."""
        raise NotImplementedError

    def remove_at(self, index: int) -> T:
        """Remove and return the item at `index` (IndexError if bad). O(n)."""
        raise NotImplementedError

    def remove(self, item: T) -> T | None:
        """Remove the first node whose value == `item`; return it or None. O(n)."""
        raise NotImplementedError
