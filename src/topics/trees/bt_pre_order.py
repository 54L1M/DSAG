"""Binary tree pre-order traversal (node, left, right)."""

from __future__ import annotations

from common.types import BinaryNode


def pre_order(root: BinaryNode | None) -> list[int]:
    """Return node values in **pre-order**: visit the node, then left, then right.

    Recursive shape: append `root.value`, then recurse left, then recurse right.
    An empty tree (None) yields an empty list.

    Time: O(n). Space: O(h) for the recursion stack (h = tree height).
    """
    raise NotImplementedError  # remove this line and implement
