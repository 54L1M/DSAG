"""Shared test helpers: tree builders, sample graphs, and validators."""

from __future__ import annotations

from collections import deque

from common.types import (
    BinaryNode,
    WeightedAdjacencyList,
    WeightedAdjacencyMatrix,
)

# --- Binary tree builders --------------------------------------------------


def build_tree(level_order: list[int | None]) -> BinaryNode | None:
    """Build a binary tree from a level-order list (None = missing child)."""
    if not level_order or level_order[0] is None:
        return None
    root = BinaryNode(level_order[0])
    q: deque[BinaryNode] = deque([root])
    i = 1
    while q and i < len(level_order):
        node = q.popleft()
        if i < len(level_order):
            v = level_order[i]
            i += 1
            if v is not None:
                node.left = BinaryNode(v)
                q.append(node.left)
        if i < len(level_order):
            v = level_order[i]
            i += 1
            if v is not None:
                node.right = BinaryNode(v)
                q.append(node.right)
    return root


def build_bst(values: list[int]) -> BinaryNode | None:
    """Insert `values` (in order) into a binary search tree and return the root."""
    root: BinaryNode | None = None
    for v in values:
        root = _bst_insert(root, v)
    return root


def _bst_insert(root: BinaryNode | None, value: int) -> BinaryNode:
    if root is None:
        return BinaryNode(value)
    if value < root.value:
        root.left = _bst_insert(root.left, value)
    else:
        root.right = _bst_insert(root.right, value)
    return root


# A BST shaped like:
#           20
#         /    \
#        10     50
#       /  \   /  \
#      5   15 30  100
SAMPLE_TREE_LEVEL_ORDER: list[int | None] = [20, 10, 50, 5, 15, 30, 100]


# --- Graph fixtures --------------------------------------------------------

# Directed, weighted adjacency list (edges as (to, weight)).
# Shortest path 0 -> 6 is [0, 1, 4, 5, 6] with total weight 7.
SAMPLE_LIST: WeightedAdjacencyList = [
    [(1, 3), (2, 1)],  # 0
    [(0, 3), (2, 4), (4, 1)],  # 1
    [(1, 4), (3, 7), (0, 1)],  # 2
    [(2, 7), (4, 5), (6, 1)],  # 3
    [(1, 1), (3, 5), (5, 2)],  # 4
    [(6, 1), (4, 2)],  # 5
    [(3, 1), (5, 1), (7, 1)],  # 6
    [(6, 1)],  # 7
]

# Directed, unweighted-as-weighted adjacency matrix (0 means "no edge").
# 0 -> 1, 0 -> 2, 1 -> 3, 2 -> 3.  BFS 0 -> 3 yields [0, 1, 3].
SAMPLE_MATRIX: WeightedAdjacencyMatrix = [
    [0, 1, 1, 0],
    [0, 0, 0, 1],
    [0, 0, 0, 1],
    [0, 0, 0, 0],
]

# Undirected, weighted adjacency list for MST tests.
# Minimum spanning tree weight is 4: edges 0-1 (1), 1-2 or 0-2 (2), 2-3 (1).
SAMPLE_UNDIRECTED: WeightedAdjacencyList = [
    [(1, 1), (2, 2), (3, 4)],  # 0
    [(0, 1), (2, 2)],  # 1
    [(1, 2), (0, 2), (3, 1)],  # 2
    [(2, 1), (0, 4)],  # 3
]
SAMPLE_UNDIRECTED_MST_WEIGHT = 4


# --- Validators ------------------------------------------------------------


def is_valid_list_path(
    graph: WeightedAdjacencyList, path: list[int], source: int, needle: int
) -> bool:
    """True if `path` is a real walk from `source` to `needle` in `graph`."""
    if not path or path[0] != source or path[-1] != needle:
        return False
    return all(any(to == b for to, _w in graph[a]) for a, b in zip(path, path[1:], strict=False))


def collect_mst_edges(mst: WeightedAdjacencyList) -> set[tuple[int, int, int]]:
    """Return undirected MST edges as a set of (min_node, max_node, weight)."""
    edges: set[tuple[int, int, int]] = set()
    for frm, adj in enumerate(mst):
        for to, weight in adj:
            edges.add((min(frm, to), max(frm, to), weight))
    return edges


def is_connected_spanning_tree(mst: WeightedAdjacencyList, n: int) -> bool:
    """True if `mst` connects all `n` nodes with exactly n-1 undirected edges."""
    edges = collect_mst_edges(mst)
    if len(edges) != n - 1:
        return False
    seen = {0}
    stack = [0]
    while stack:
        cur = stack.pop()
        for to, _w in mst[cur]:
            if to not in seen:
                seen.add(to)
                stack.append(to)
    return len(seen) == n
