"""Depth-first search on a weighted adjacency list — find a path."""

from __future__ import annotations

from common.types import WeightedAdjacencyList


def dfs(graph: WeightedAdjacencyList, source: int, needle: int) -> list[int] | None:
    """Return a path (list of node indices) from `source` to `needle`, or None.

    `graph[n]` is a list of (neighbour, weight) edges leaving node `n`. Walk
    depth-first with recursion, tracking visited nodes and the current path.
    When you reach `needle`, the path you built is the answer. Backtrack (pop)
    when a branch dead-ends.

    Any valid path is acceptable (DFS does not guarantee the shortest one).
    Time: O(V + E). Space: O(V).
    """
    raise NotImplementedError  # remove this line and implement
