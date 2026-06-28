"""Binary tree in-order traversal (left, node, right)."""

from __future__ import annotations

from common.types import BinaryNode


def in_order(root: BinaryNode | None) -> list[int]:
    """Return node values in **in-order**: left, then the node, then right.

    Recursive shape: recurse left, append `root.value`, recurse right. For a
    binary *search* tree this yields the values in ascending sorted order.

    Time: O(n). Space: O(h).
    """
    raise NotImplementedError  # remove this line and implement
