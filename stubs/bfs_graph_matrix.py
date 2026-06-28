"""Breadth-first search on a weighted adjacency matrix — find a path."""

from __future__ import annotations

from common.types import WeightedAdjacencyMatrix


def bfs(graph: WeightedAdjacencyMatrix, source: int, needle: int) -> list[int] | None:
    """Return a path (list of node indices) from `source` to `needle`, or None.

    `graph[from][to]` is the edge weight, or 0 when there is no edge. Explore
    breadth-first with a queue, recording for each visited node which node you
    came *from* (a `prev` array). When you dequeue `needle`, walk the `prev`
    chain backwards from `needle` to `source` and reverse it to get the path.

    Time: O(V^2) for a matrix. Space: O(V).
    """
    raise NotImplementedError  # remove this line and implement
