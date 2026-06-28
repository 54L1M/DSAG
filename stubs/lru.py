"""LRU cache — evict the least-recently-used entry when full."""

from __future__ import annotations

from typing import Generic, TypeVar

K = TypeVar("K")
V = TypeVar("V")


class LRU(Generic[K, V]):
    """A fixed-capacity cache that evicts the least recently used key.

    The classic design pairs a dict (key -> node) for O(1) lookup with a
    doubly linked list ordering nodes from most- to least-recently used. On
    every `get`/`update`, move the touched node to the "most recent" end. When
    inserting beyond `capacity`, drop the node at the "least recent" end.

    Build the linked list yourself to get the full lesson (an OrderedDict would
    hide the interesting part).
    """

    def __init__(self, capacity: int) -> None:
        self.capacity: int = capacity
        self.length: int = 0
        raise NotImplementedError  # remove this line and implement

    def update(self, key: K, value: V) -> None:
        """Insert or update `key` -> `value` and mark it most-recently used.

        If inserting exceeds `capacity`, evict the least-recently-used entry.
        O(1).
        """
        raise NotImplementedError

    def get(self, key: K) -> V | None:
        """Return the value for `key` (and mark it most-recently used), else None. O(1)."""
        raise NotImplementedError
