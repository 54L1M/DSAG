"""Binary tree post-order traversal (left, right, node)."""

from __future__ import annotations

from common.types import BinaryNode


def post_order(root: BinaryNode | None) -> list[int]:
    """Return node values in **post-order**: left, then right, then the node.

    Recursive shape: recurse left, recurse right, append `root.value`. Useful
    when you must process children before their parent (e.g. freeing a tree).

    Time: O(n). Space: O(h).
    """
    raise NotImplementedError  # remove this line and implement
