"""Dijkstra's shortest path on a weighted adjacency list."""

from __future__ import annotations

from common.types import WeightedAdjacencyList


def dijkstra(graph: WeightedAdjacencyList, source: int, sink: int) -> list[int]:
    """Return the lowest-weight path from `source` to `sink` as a list of nodes.

    `graph[n]` is a list of (neighbour, weight) edges (weights are non-negative).
    Maintain a `dist` array (distance from source, start at infinity) and a
    `prev` array. Repeatedly pick the unvisited node with the smallest known
    distance, relax its edges (update a neighbour if going through this node is
    cheaper), and mark it visited. Reconstruct the path from `prev`.

    A heap (`heapq`) makes picking the nearest node efficient. Return an empty
    list if `sink` is unreachable.

    Time: O((V + E) log V) with a heap. Space: O(V).
    """
    raise NotImplementedError  # remove this line and implement
