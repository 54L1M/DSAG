"""Doubly linked list — nodes chained by both `prev` and `next` pointers."""

from __future__ import annotations

from typing import Generic, TypeVar

T = TypeVar("T")


class DoublyLinkedList(Generic[T]):
    """A list backed by doubly-linked nodes (None <- ... <-> ... -> None).

    Same public interface as the singly-linked list, but each node also points
    backwards, which makes removal and end-operations cleaner. Indices are
    0-based; out-of-range get/insert/remove_at raise IndexError.

    Implement the node plumbing yourself (don't wrap a Python list).
    """

    def __init__(self) -> None:
        self.length: int = 0
        # Suggested: self.head and self.tail node references.
        raise NotImplementedError  # remove this line and implement

    def prepend(self, item: T) -> None:
        """Insert `item` at the front. O(1)."""
        raise NotImplementedError

    def append(self, item: T) -> None:
        """Insert `item` at the end. O(1)."""
        raise NotImplementedError

    def insert_at(self, item: T, index: int) -> None:
        """Insert `item` so it ends up at position `index`. O(n) to walk, O(1) to link.

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
