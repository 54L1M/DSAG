"""Shared data types used by several exercises.

These are *given* to you — you do not implement them. They define the shape of
the inputs your functions receive (binary tree nodes, graph representations,
maze points). Import them in your stubs and solutions, e.g.::

    from common.types import BinaryNode
"""

from __future__ import annotations

from dataclasses import dataclass, field

# --- Binary trees ----------------------------------------------------------


@dataclass
class BinaryNode:
    """A node in a binary tree.

    For a binary *search* tree, the invariant is: everything in ``left`` is
    smaller than ``value`` and everything in ``right`` is larger.
    """

    value: int
    left: BinaryNode | None = None
    right: BinaryNode | None = None


# --- Graphs ----------------------------------------------------------------

# An edge in a weighted adjacency list: (destination_node, weight).
GraphEdge = tuple[int, int]

# adjacency_list[node] -> list of edges leaving `node`.
WeightedAdjacencyList = list[list[GraphEdge]]

# matrix[from][to] == weight, or 0 when there is no edge.
WeightedAdjacencyMatrix = list[list[int]]


# --- Maze ------------------------------------------------------------------

# A point in the maze grid as (row, col).
Point = tuple[int, int]


# --- Linked-list / generic node (handy if you want a typed node) -----------


@dataclass
class Node:
    """A generic singly-linked node (optional helper for linked-list exercises)."""

    value: object
    next: Node | None = None


@dataclass
class DNode:
    """A generic doubly-linked node (optional helper for linked-list exercises)."""

    value: object
    prev: DNode | None = None
    next: DNode | None = field(default=None)
