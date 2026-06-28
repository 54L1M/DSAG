"""Reference solution — dynamic array with capacity doubling."""

from __future__ import annotations

from typing import Generic, TypeVar

T = TypeVar("T")


class ArrayList(Generic[T]):
    def __init__(self, capacity: int = 2) -> None:
        self.length: int = 0
        self.capacity: int = max(1, capacity)
        self._data: list[T | None] = [None] * self.capacity

    def _ensure_capacity(self, needed: int) -> None:
        if needed <= self.capacity:
            return
        new_cap = self.capacity
        while new_cap < needed:
            new_cap *= 2
        new_data: list[T | None] = [None] * new_cap
        for i in range(self.length):
            new_data[i] = self._data[i]
        self._data = new_data
        self.capacity = new_cap

    def get(self, index: int) -> T:
        if index < 0 or index >= self.length:
            raise IndexError(index)
        return self._data[index]  # type: ignore[return-value]

    def set(self, index: int, item: T) -> None:
        if index < 0 or index >= self.length:
            raise IndexError(index)
        self._data[index] = item

    def push(self, item: T) -> None:
        self._ensure_capacity(self.length + 1)
        self._data[self.length] = item
        self.length += 1

    def pop(self) -> T | None:
        if self.length == 0:
            return None
        self.length -= 1
        value = self._data[self.length]
        self._data[self.length] = None
        return value

    def insert_at(self, item: T, index: int) -> None:
        if index < 0 or index > self.length:
            raise IndexError(index)
        self._ensure_capacity(self.length + 1)
        for i in range(self.length, index, -1):
            self._data[i] = self._data[i - 1]
        self._data[index] = item
        self.length += 1

    def remove_at(self, index: int) -> T:
        if index < 0 or index >= self.length:
            raise IndexError(index)
        value = self._data[index]
        for i in range(index, self.length - 1):
            self._data[i] = self._data[i + 1]
        self.length -= 1
        self._data[self.length] = None
        return value  # type: ignore[return-value]
