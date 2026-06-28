"""Reference solution — breadth-first (level-order) traversal."""

from __future__ import annotations

from collections import deque

from common.types import BinaryNode


def bfs(root: BinaryNode | None) -> list[int]:
    out: list[int] = []
    if root is None:
        return out
    q: deque[BinaryNode] = deque([root])
    while q:
        node = q.popleft()
        out.append(node.value)
        if node.left is not None:
            q.append(node.left)
        if node.right is not None:
            q.append(node.right)
    return out
