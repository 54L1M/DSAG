"""Reference solution — Prim's minimum spanning tree (heap-based)."""

from __future__ import annotations

import heapq

from common.types import WeightedAdjacencyList


def prims(graph: WeightedAdjacencyList) -> WeightedAdjacencyList | None:
    n = len(graph)
    if n == 0:
        return None

    mst: WeightedAdjacencyList = [[] for _ in range(n)]
    in_mst = [False] * n

    # Heap entries: (weight, from_node, to_node).
    heap: list[tuple[int, int, int]] = []

    def add_node(node: int) -> None:
        in_mst[node] = True
        for to, weight in graph[node]:
            if not in_mst[to]:
                heapq.heappush(heap, (weight, node, to))

    add_node(0)
    while heap:
        weight, frm, to = heapq.heappop(heap)
        if in_mst[to]:
            continue
        mst[frm].append((to, weight))
        mst[to].append((frm, weight))
        add_node(to)

    return mst
