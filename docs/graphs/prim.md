# Prim's Minimum Spanning Tree

> graphs · stub: `src/topics/graphs/prim.py` · test: `tests/test_prim.py`
>
> 📚 Need more detail? See the [in-depth version](prim.deep.md).

## Intuition
A **minimum spanning tree** (MST) connects every node of an undirected, weighted
graph using a subset of edges whose total weight is as small as possible (and
with no cycles). Prim's algorithm grows one tree outward from a starting node,
greedily swallowing the **cheapest edge that reaches a new node** at each step —
like laying the least expensive cable that hooks up one more building, over and
over. A min-heap of candidate edges makes "cheapest crossing edge" fast.

## How it works
The graph is an undirected `WeightedAdjacencyList`: each edge appears on **both**
endpoints. Using the fixture `SAMPLE_UNDIRECTED`, node `0` has
`[(1, 1), (2, 2), (3, 4)]`. We keep an `in_mst` flag array, a min-heap of
`(weight, from, to)` candidates, and the result `mst` (a fresh adjacency list of
the same size). Steps for `prims(SAMPLE_UNDIRECTED)`:

1. Add node `0` to the tree: mark `in_mst[0] = True` and push each of its edges
   onto the heap → `(1, 0, 1)`, `(2, 0, 2)`, `(4, 0, 3)`.
2. **Pop the cheapest** crossing edge: `(1, 0, 1)`. Node `1` is outside the
   tree, so accept it.
3. **Record the edge on both endpoints**: append `(1, 1)` to `mst[0]` and
   `(0, 1)` to `mst[1]`. Then add node `1`, pushing its outgoing edges.
4. Pop next-cheapest. Edges into already-in-tree nodes are skipped as stale.
   We add `2` (weight 2) and finally `3` via `2 -> 3` (weight 1).
5. Stop when the heap is empty (all reachable nodes are in the tree).

The chosen edges are `0-1 (1)`, `0-2` or `1-2 (2)`, and `2-3 (1)`, total weight
**4** (`SAMPLE_UNDIRECTED_MST_WEIGHT`). The returned `mst` is an adjacency list
of size `n` with each edge stored on both sides. Return `None` if the graph is
empty.

## Complexity
- **Time:** O(E log V)
- **Space:** O(V + E)

Each edge can be pushed to the heap once, and each heap operation is O(log V);
the heap and the output adjacency list together hold O(V + E).

## Common pitfalls
- Adding an edge to a node **already in the tree** — always re-check `in_mst[to]`
  *after* popping, since the entry may have gone stale while it sat in the heap.
- Recording the edge on only **one** endpoint — the MST must be undirected, so
  append to both `mst[from]` and `mst[to]`.
- Pushing edges to nodes already in the tree (harmless if you skip them on pop,
  but cleaner to skip when pushing too).
- Returning the **total weight** instead of the MST adjacency list.
- Forgetting the empty-graph case (`n == 0` → return `None`, not `[]`).

## Your task
Implement in `src/topics/graphs/prim.py`, then run:

```bash
uv run pytest -k prim
```

Peek at `solutions/prim.py` only once you've given it a real attempt.
