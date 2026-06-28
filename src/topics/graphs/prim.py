"""Prim's algorithm — minimum spanning tree of a weighted graph."""

from __future__ import annotations

from common.types import WeightedAdjacencyList


def prims(graph: WeightedAdjacencyList) -> WeightedAdjacencyList | None:
    """Return a minimum spanning tree of `graph` as an adjacency list, or None.

    `graph[n]` is a list of (neighbour, weight) edges (undirected: each edge
    appears on both endpoints). Grow a tree from node 0: repeatedly add the
    cheapest edge that connects a node already in the tree to one outside it,
    until every reachable node is included. A heap of candidate edges keyed by
    weight makes "cheapest crossing edge" efficient.

    The returned MST is itself an adjacency list of the same size, with each
    chosen edge recorded on *both* endpoints. Return None if the graph is empty.

    Time: O(E log V). Space: O(V + E).
    """
    raise NotImplementedError  # remove this line and implement
