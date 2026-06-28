"""Depth-first search on a binary search tree (BST find)."""

from __future__ import annotations

from common.types import BinaryNode


def find(root: BinaryNode | None, value: int) -> bool:
    """Return True if `value` exists in the BST rooted at `root`.

    Exploit the BST invariant instead of scanning every node: if `value` equals
    the current node you are done; if it is smaller, go left; if larger, go
    right. Hitting None means the value is absent.

    Time: O(h) — O(log n) for a balanced tree, O(n) worst. Space: O(h).
    """
    raise NotImplementedError  # remove this line and implement
