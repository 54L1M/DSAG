"""Compare two binary trees for structural + value equality."""

from __future__ import annotations

from common.types import BinaryNode


def compare(a: BinaryNode | None, b: BinaryNode | None) -> bool:
    """Return True iff `a` and `b` have the same shape and the same values.

    Recurse on both trees in lockstep:
      * if both are None -> equal
      * if exactly one is None -> not equal
      * if the values differ -> not equal
      * otherwise compare left subtrees AND right subtrees

    Time: O(n). Space: O(h).
    """
    raise NotImplementedError  # remove this line and implement
