"""Reference solution — array-backed binary min-heap."""

from __future__ import annotations


class MinHeap:
    def __init__(self) -> None:
        self.length: int = 0
        self.data: list[int] = []

    def insert(self, value: int) -> None:
        self.data.append(value)
        self.length += 1
        self._bubble_up(self.length - 1)

    def delete(self) -> int | None:
        if self.length == 0:
            return None
        top = self.data[0]
        self.length -= 1
        last = self.data.pop()
        if self.length > 0:
            self.data[0] = last
            self._bubble_down(0)
        return top

    def _bubble_up(self, idx: int) -> None:
        while idx > 0:
            parent = (idx - 1) // 2
            if self.data[idx] >= self.data[parent]:
                break
            self.data[idx], self.data[parent] = self.data[parent], self.data[idx]
            idx = parent

    def _bubble_down(self, idx: int) -> None:
        while True:
            left = 2 * idx + 1
            right = 2 * idx + 2
            smallest = idx
            if left < self.length and self.data[left] < self.data[smallest]:
                smallest = left
            if right < self.length and self.data[right] < self.data[smallest]:
                smallest = right
            if smallest == idx:
                break
            self.data[idx], self.data[smallest] = self.data[smallest], self.data[idx]
            idx = smallest
