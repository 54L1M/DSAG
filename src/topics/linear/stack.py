"""Stack — last in, first out (LIFO)."""

from __future__ import annotations

from typing import Generic, TypeVar

T = TypeVar("T")


class Stack(Generic[T]):
    """A LIFO stack backed by a singly-linked list (push/pop at the head).

    Keep a single `head` pointer to the top of the stack. push, pop and peek
    are all O(1). Build it from nodes rather than wrapping a Python list.
    """

    def __init__(self) -> None:
        self.length: int = 0
        raise NotImplementedError  # remove this line and implement

    def push(self, item: T) -> None:
        """Push `item` onto the top of the stack. O(1)."""
        raise NotImplementedError

    def pop(self) -> T | None:
        """Remove and return the top item, or None if empty. O(1)."""
        raise NotImplementedError

    def peek(self) -> T | None:
        """Return the top item without removing it, or None if empty. O(1)."""
        raise NotImplementedError
