"""Reference solution — HashMap with separate chaining + resize."""

from __future__ import annotations

from typing import Generic, TypeVar

K = TypeVar("K")
V = TypeVar("V")


class HashMap(Generic[K, V]):
    def __init__(self, capacity: int = 8) -> None:
        self.length: int = 0
        self.capacity: int = max(1, capacity)
        self._buckets: list[list[tuple[K, V]]] = [[] for _ in range(self.capacity)]

    def _index(self, key: K) -> int:
        return hash(key) % self.capacity

    def _resize(self) -> None:
        old = self._buckets
        self.capacity *= 2
        self._buckets = [[] for _ in range(self.capacity)]
        for bucket in old:
            for k, v in bucket:
                self._buckets[hash(k) % self.capacity].append((k, v))

    def set(self, key: K, value: V) -> None:
        bucket = self._buckets[self._index(key)]
        for i, (k, _v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return
        bucket.append((key, value))
        self.length += 1
        if self.length > self.capacity * 0.75:
            self._resize()

    def get(self, key: K) -> V | None:
        bucket = self._buckets[self._index(key)]
        for k, v in bucket:
            if k == key:
                return v
        return None

    def remove(self, key: K) -> V | None:
        bucket = self._buckets[self._index(key)]
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket.pop(i)
                self.length -= 1
                return v
        return None
