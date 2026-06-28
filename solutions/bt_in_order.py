"""Reference solution — in-order traversal."""

from __future__ import annotations

from common.types import BinaryNode


def in_order(root: BinaryNode | None) -> list[int]:
    out: list[int] = []
    _walk(root, out)
    return out


def _walk(node: BinaryNode | None, out: list[int]) -> None:
    if node is None:
        return
    _walk(node.left, out)
    out.append(node.value)
    _walk(node.right, out)
