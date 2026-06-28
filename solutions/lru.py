"""Reference solution — LRU cache (dict + doubly linked list)."""

from __future__ import annotations

from typing import Generic, TypeVar

K = TypeVar("K")
V = TypeVar("V")


class _Node(Generic[K, V]):
    __slots__ = ("key", "value", "prev", "next")

    def __init__(self, key: K, value: V) -> None:
        self.key: K = key
        self.value: V = value
        self.prev: _Node[K, V] | None = None
        self.next: _Node[K, V] | None = None


class LRU(Generic[K, V]):
    def __init__(self, capacity: int) -> None:
        self.capacity: int = capacity
        self.length: int = 0
        self._lookup: dict[K, _Node[K, V]] = {}
        self._head: _Node[K, V] | None = None  # most recently used
        self._tail: _Node[K, V] | None = None  # least recently used

    def update(self, key: K, value: V) -> None:
        node = self._lookup.get(key)
        if node is not None:
            node.value = value
            self._detach(node)
            self._prepend(node)
            return

        node = _Node(key, value)
        self._lookup[key] = node
        self._prepend(node)
        self.length += 1

        if self.capacity > 0 and self.length > self.capacity:
            self._evict()

    def get(self, key: K) -> V | None:
        node = self._lookup.get(key)
        if node is None:
            return None
        self._detach(node)
        self._prepend(node)
        return node.value

    # --- internal doubly-linked-list helpers ---

    def _prepend(self, node: _Node[K, V]) -> None:
        node.prev = None
        node.next = self._head
        if self._head is not None:
            self._head.prev = node
        self._head = node
        if self._tail is None:
            self._tail = node

    def _detach(self, node: _Node[K, V]) -> None:
        if node.prev is not None:
            node.prev.next = node.next
        else:
            self._head = node.next
        if node.next is not None:
            node.next.prev = node.prev
        else:
            self._tail = node.prev
        node.prev = node.next = None

    def _evict(self) -> None:
        lru = self._tail
        if lru is None:
            return
        self._detach(lru)
        del self._lookup[lru.key]
        self.length -= 1
