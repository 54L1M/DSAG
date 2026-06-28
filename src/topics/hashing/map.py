"""HashMap — key/value store built on hashing + separate chaining."""

from __future__ import annotations

from typing import Generic, TypeVar

K = TypeVar("K")
V = TypeVar("V")


class HashMap(Generic[K, V]):
    """A hash map you build yourself (don't wrap Python's dict).

    Use an array of buckets; hash the key (Python's built-in `hash()` is fine)
    and mod by the number of buckets to pick one. Handle collisions with
    separate chaining: each bucket holds a list of (key, value) pairs. Resize
    (e.g. double the buckets and rehash) when the load factor gets high to keep
    operations close to O(1).
    """

    def __init__(self, capacity: int = 8) -> None:
        self.length: int = 0
        self.capacity: int = capacity
        raise NotImplementedError  # remove this line and implement

    def set(self, key: K, value: V) -> None:
        """Insert or update `key` -> `value`. Amortized O(1)."""
        raise NotImplementedError

    def get(self, key: K) -> V | None:
        """Return the value for `key`, or None if absent. O(1) average."""
        raise NotImplementedError

    def remove(self, key: K) -> V | None:
        """Remove `key`; return its old value, or None if absent. O(1) average."""
        raise NotImplementedError
