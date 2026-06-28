"""Reference solution — singly linked list."""

from __future__ import annotations

from typing import Generic, TypeVar

T = TypeVar("T")


class _Node(Generic[T]):
    __slots__ = ("value", "next")

    def __init__(self, value: T) -> None:
        self.value: T = value
        self.next: _Node[T] | None = None


class SinglyLinkedList(Generic[T]):
    def __init__(self) -> None:
        self.length: int = 0
        self.head: _Node[T] | None = None
        self.tail: _Node[T] | None = None

    def prepend(self, item: T) -> None:
        node = _Node(item)
        node.next = self.head
        self.head = node
        if self.tail is None:
            self.tail = node
        self.length += 1

    def append(self, item: T) -> None:
        node = _Node(item)
        if self.tail is None:
            self.head = self.tail = node
        else:
            self.tail.next = node
            self.tail = node
        self.length += 1

    def insert_at(self, item: T, index: int) -> None:
        if index < 0 or index > self.length:
            raise IndexError(index)
        if index == 0:
            self.prepend(item)
            return
        if index == self.length:
            self.append(item)
            return
        prev = self._node_at(index - 1)
        node = _Node(item)
        node.next = prev.next
        prev.next = node
        self.length += 1

    def get(self, index: int) -> T:
        return self._node_at(index).value

    def remove_at(self, index: int) -> T:
        if index < 0 or index >= self.length:
            raise IndexError(index)
        if index == 0:
            assert self.head is not None
            node = self.head
            self.head = node.next
            if self.head is None:
                self.tail = None
            self.length -= 1
            return node.value
        prev = self._node_at(index - 1)
        node = prev.next
        assert node is not None
        prev.next = node.next
        if node is self.tail:
            self.tail = prev
        self.length -= 1
        return node.value

    def remove(self, item: T) -> T | None:
        prev: _Node[T] | None = None
        cur = self.head
        while cur is not None:
            if cur.value == item:
                if prev is None:
                    self.head = cur.next
                else:
                    prev.next = cur.next
                if cur is self.tail:
                    self.tail = prev
                self.length -= 1
                return cur.value
            prev, cur = cur, cur.next
        return None

    def _node_at(self, index: int) -> _Node[T]:
        if index < 0 or index >= self.length:
            raise IndexError(index)
        cur = self.head
        for _ in range(index):
            assert cur is not None
            cur = cur.next
        assert cur is not None
        return cur
