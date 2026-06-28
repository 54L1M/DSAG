"""Reference solution — FIFO queue (linked list)."""

from __future__ import annotations

from typing import Generic, TypeVar

T = TypeVar("T")


class _Node(Generic[T]):
    __slots__ = ("value", "next")

    def __init__(self, value: T) -> None:
        self.value: T = value
        self.next: _Node[T] | None = None


class Queue(Generic[T]):
    def __init__(self) -> None:
        self.length: int = 0
        self.head: _Node[T] | None = None
        self.tail: _Node[T] | None = None

    def enqueue(self, item: T) -> None:
        node = _Node(item)
        if self.tail is None:
            self.head = self.tail = node
        else:
            self.tail.next = node
            self.tail = node
        self.length += 1

    def dequeue(self) -> T | None:
        if self.head is None:
            return None
        node = self.head
        self.head = node.next
        if self.head is None:
            self.tail = None
        self.length -= 1
        return node.value

    def peek(self) -> T | None:
        return self.head.value if self.head is not None else None
