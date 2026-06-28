"""Queue — first in, first out (FIFO)."""

from __future__ import annotations

from typing import Generic, TypeVar

T = TypeVar("T")


class Queue(Generic[T]):
    """A FIFO queue backed by a singly-linked list with head and tail pointers.

    enqueue adds at the tail, dequeue removes from the head — both O(1). Build
    it from nodes (don't use list.pop(0), which is O(n) and defeats the lesson).
    """

    def __init__(self) -> None:
        self.length: int = 0
        raise NotImplementedError  # remove this line and implement

    def enqueue(self, item: T) -> None:
        """Add `item` to the back of the queue. O(1)."""
        raise NotImplementedError

    def dequeue(self) -> T | None:
        """Remove and return the front item, or None if empty. O(1)."""
        raise NotImplementedError

    def peek(self) -> T | None:
        """Return the front item without removing it, or None if empty. O(1)."""
        raise NotImplementedError
