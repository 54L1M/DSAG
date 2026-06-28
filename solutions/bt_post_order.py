"""Reference solution — post-order traversal."""

from __future__ import annotations

from common.types import BinaryNode


def post_order(root: BinaryNode | None) -> list[int]:
    out: list[int] = []
    _walk(root, out)
    return out


def _walk(node: BinaryNode | None, out: list[int]) -> None:
    if node is None:
        return
    _walk(node.left, out)
    _walk(node.right, out)
    out.append(node.value)
