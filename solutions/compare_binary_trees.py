"""Reference solution — compare two binary trees."""

from __future__ import annotations

from common.types import BinaryNode


def compare(a: BinaryNode | None, b: BinaryNode | None) -> bool:
    if a is None and b is None:
        return True
    if a is None or b is None:
        return False
    if a.value != b.value:
        return False
    return compare(a.left, b.left) and compare(a.right, b.right)
