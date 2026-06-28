"""Reference solution — LIFO stack (linked list)."""

from __future__ import annotations

from typing import Generic, TypeVar

T = TypeVar("T")


class _Node(Generic[T]):
    __slots__ = ("value", "next")

    def __init__(self, value: T) -> None:
        self.value: T = value
        self.next: _Node[T] | None = None


class Stack(Generic[T]):
    def __init__(self) -> None:
        self.length: int = 0
        self.head: _Node[T] | None = None

    def push(self, item: T) -> None:
        node = _Node(item)
        node.next = self.head
        self.head = node
        self.length += 1

    def pop(self) -> T | None:
        if self.head is None:
            return None
        node = self.head
        self.head = node.next
        self.length -= 1
        return node.value

    def peek(self) -> T | None:
        return self.head.value if self.head is not None else None
