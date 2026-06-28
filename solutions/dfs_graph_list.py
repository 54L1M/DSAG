"""Reference solution — DFS path on a weighted adjacency list."""

from __future__ import annotations

from common.types import WeightedAdjacencyList


def dfs(graph: WeightedAdjacencyList, source: int, needle: int) -> list[int] | None:
    seen = [False] * len(graph)
    path: list[int] = []
    if _walk(graph, source, needle, seen, path):
        return path
    return None


def _walk(
    graph: WeightedAdjacencyList,
    curr: int,
    needle: int,
    seen: list[bool],
    path: list[int],
) -> bool:
    if seen[curr]:
        return False
    seen[curr] = True
    path.append(curr)

    if curr == needle:
        return True

    for to, _weight in graph[curr]:
        if _walk(graph, to, needle, seen, path):
            return True

    path.pop()
    return False
