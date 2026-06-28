"""Reference solution — pre-order traversal."""

from __future__ import annotations

from common.types import BinaryNode


def pre_order(root: BinaryNode | None) -> list[int]:
    out: list[int] = []
    _walk(root, out)
    return out


def _walk(node: BinaryNode | None, out: list[int]) -> None:
    if node is None:
        return
    out.append(node.value)
    _walk(node.left, out)
    _walk(node.right, out)
