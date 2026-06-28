"""Reference solution — BFS path on a weighted adjacency matrix."""

from __future__ import annotations

from collections import deque

from common.types import WeightedAdjacencyMatrix


def bfs(graph: WeightedAdjacencyMatrix, source: int, needle: int) -> list[int] | None:
    n = len(graph)
    seen = [False] * n
    prev = [-1] * n

    seen[source] = True
    q: deque[int] = deque([source])
    while q:
        curr = q.popleft()
        if curr == needle:
            break
        for to in range(n):
            if graph[curr][to] == 0 or seen[to]:
                continue
            seen[to] = True
            prev[to] = curr
            q.append(to)

    if not seen[needle]:
        return None

    # Reconstruct path by walking prev backwards.
    path: list[int] = []
    at = needle
    while at != -1:
        path.append(at)
        at = prev[at]
    path.reverse()
    return path
