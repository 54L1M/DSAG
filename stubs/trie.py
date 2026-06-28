"""Trie (prefix tree) — store words for fast prefix lookups / autocomplete."""

from __future__ import annotations


class Trie:
    """A prefix tree over lowercase words.

    Each node has up to 26 children (one per letter) and a flag marking the end
    of a word. Suggested node shape: a dict mapping char -> child node plus a
    boolean `is_word`.
    """

    def __init__(self) -> None:
        raise NotImplementedError  # remove this line and implement

    def insert(self, word: str) -> None:
        """Add `word` to the trie. O(len(word))."""
        raise NotImplementedError

    def delete(self, word: str) -> None:
        """Remove `word` if present (a no-op if absent). O(len(word)).

        It is fine to just unset the end-of-word flag; pruning now-empty nodes
        is a nice extra but not required.
        """
        raise NotImplementedError

    def contains(self, word: str) -> bool:
        """Return True if the exact `word` was inserted. O(len(word))."""
        raise NotImplementedError

    def starts_with(self, prefix: str) -> list[str]:
        """Return all inserted words beginning with `prefix`, in sorted order.

        Walk to the prefix node, then DFS collecting every completed word below
        it. Order the result lexicographically.
        """
        raise NotImplementedError
