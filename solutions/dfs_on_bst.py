"""Reference solution — DFS find on a binary search tree."""

from __future__ import annotations

from common.types import BinaryNode


def find(root: BinaryNode | None, value: int) -> bool:
    node = root
    while node is not None:
        if value == node.value:
            return True
        node = node.left if value < node.value else node.right
    return False
