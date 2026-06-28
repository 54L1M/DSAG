"""Reference solution — doubly linked list."""

from __future__ import annotations

from typing import Generic, TypeVar

T = TypeVar("T")


class _Node(Generic[T]):
    __slots__ = ("value", "prev", "next")

    def __init__(self, value: T) -> None:
        self.value: T = value
        self.prev: _Node[T] | None = None
        self.next: _Node[T] | None = None


class DoublyLinkedList(Generic[T]):
    def __init__(self) -> None:
        self.length: int = 0
        self.head: _Node[T] | None = None
        self.tail: _Node[T] | None = None

    def prepend(self, item: T) -> None:
        node = _Node(item)
        node.next = self.head
        if self.head is not None:
            self.head.prev = node
        self.head = node
        if self.tail is None:
            self.tail = node
        self.length += 1

    def append(self, item: T) -> None:
        node = _Node(item)
        node.prev = self.tail
        if self.tail is not None:
            self.tail.next = node
        self.tail = node
        if self.head is None:
            self.head = node
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
        cur = self._node_at(index)
        prev = cur.prev
        assert prev is not None
        node = _Node(item)
        node.prev = prev
        node.next = cur
        prev.next = node
        cur.prev = node
        self.length += 1

    def get(self, index: int) -> T:
        return self._node_at(index).value

    def remove_at(self, index: int) -> T:
        return self._remove_node(self._node_at(index))

    def remove(self, item: T) -> T | None:
        cur = self.head
        while cur is not None:
            if cur.value == item:
                return self._remove_node(cur)
            cur = cur.next
        return None

    def _remove_node(self, node: _Node[T]) -> T:
        if node.prev is not None:
            node.prev.next = node.next
        else:
            self.head = node.next
        if node.next is not None:
            node.next.prev = node.prev
        else:
            self.tail = node.prev
        self.length -= 1
        return node.value

    def _node_at(self, index: int) -> _Node[T]:
        if index < 0 or index >= self.length:
            raise IndexError(index)
        # Walk from whichever end is closer.
        if index <= self.length // 2:
            cur = self.head
            for _ in range(index):
                assert cur is not None
                cur = cur.next
        else:
            cur = self.tail
            for _ in range(self.length - 1 - index):
                assert cur is not None
                cur = cur.prev
        assert cur is not None
        return cur
