"""Reference solution — Dijkstra's shortest path (heap-based)."""

from __future__ import annotations

import heapq
import math

from common.types import WeightedAdjacencyList


def dijkstra(graph: WeightedAdjacencyList, source: int, sink: int) -> list[int]:
    n = len(graph)
    dist = [math.inf] * n
    prev = [-1] * n
    dist[source] = 0

    # Heap of (distance, node). Stale entries are filtered on pop.
    heap: list[tuple[float, int]] = [(0, source)]
    visited = [False] * n

    while heap:
        d, curr = heapq.heappop(heap)
        if visited[curr]:
            continue
        visited[curr] = True
        if curr == sink:
            break
        for to, weight in graph[curr]:
            if visited[to]:
                continue
            nd = d + weight
            if nd < dist[to]:
                dist[to] = nd
                prev[to] = curr
                heapq.heappush(heap, (nd, to))

    if dist[sink] == math.inf:
        return []

    path: list[int] = []
    at = sink
    while at != -1:
        path.append(at)
        at = prev[at]
    path.reverse()
    return path
