"""Binary tree breadth-first (level-order) traversal."""

from __future__ import annotations

from common.types import BinaryNode


def bfs(root: BinaryNode | None) -> list[int]:
    """Return node values level by level, left to right (breadth-first).

    Use a queue: start with the root, then repeatedly pop the front node,
    record its value, and enqueue its left then right children. `collections.deque`
    is the right tool (popleft is O(1)).

    Time: O(n). Space: O(n) for the queue.
    """
    raise NotImplementedError  # remove this line and implement
