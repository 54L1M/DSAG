"""Reference solution — trie (prefix tree)."""

from __future__ import annotations


class _TrieNode:
    __slots__ = ("children", "is_word")

    def __init__(self) -> None:
        self.children: dict[str, _TrieNode] = {}
        self.is_word: bool = False


class Trie:
    def __init__(self) -> None:
        self.root = _TrieNode()

    def insert(self, word: str) -> None:
        node = self.root
        for ch in word:
            node = node.children.setdefault(ch, _TrieNode())
        node.is_word = True

    def delete(self, word: str) -> None:
        node = self._find_node(word)
        if node is not None:
            node.is_word = False

    def contains(self, word: str) -> bool:
        node = self._find_node(word)
        return node is not None and node.is_word

    def starts_with(self, prefix: str) -> list[str]:
        node = self._find_node(prefix)
        if node is None:
            return []
        out: list[str] = []
        self._collect(node, prefix, out)
        out.sort()
        return out

    def _find_node(self, s: str) -> _TrieNode | None:
        node = self.root
        for ch in s:
            nxt = node.children.get(ch)
            if nxt is None:
                return None
            node = nxt
        return node

    def _collect(self, node: _TrieNode, prefix: str, out: list[str]) -> None:
        if node.is_word:
            out.append(prefix)
        for ch, child in node.children.items():
            self._collect(child, prefix + ch, out)
