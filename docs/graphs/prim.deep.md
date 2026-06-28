# Prim's Minimum Spanning Tree — In Depth

> In-depth companion · graphs · stub: `src/topics/graphs/prim.py` · test: `tests/test_prim.py`
>
> New here? Read the [quick version](prim.md) first.

## The mental model

A **spanning tree** of a connected, undirected graph is a subset of edges that
touches every node with no cycles — exactly `V - 1` edges. A **minimum** spanning
tree (MST) is the spanning tree whose edges have the smallest possible total
weight. Think: connect every building with cable for the least total cost, no
redundant loops.

Prim's algorithm **grows one tree outward from a starting node** (here, node 0).
At each step it adds the **cheapest edge that connects a node already in the tree
to a node not yet in the tree** — the cheapest *crossing* edge. A min-heap of
candidate edges makes "cheapest crossing edge" fast.

Bookkeeping:

- `in_mst[node]` — is this node already in the growing tree?
- a min-heap of candidate edges `(weight, from, to)`.
- `mst` — the result: a fresh `WeightedAdjacencyList` of size `n`, with each
  chosen edge recorded on **both** endpoints (it is undirected).

The graph is an undirected `WeightedAdjacencyList`, so every edge appears twice
(once on each endpoint). Fixture `SAMPLE_UNDIRECTED`:

```
        1
   (0) --- (1)
   | \      |
  2|  \4    |2          (every edge listed on BOTH endpoints below)
   |   \    |
  (2) --+-- (1 via 2)
   |  2
  1|
   v
  (3)
```

```python
SAMPLE_UNDIRECTED = [
    [(1, 1), (2, 2), (3, 4)],   # 0
    [(0, 1), (2, 2)],           # 1
    [(1, 2), (0, 2), (3, 1)],   # 2
    [(2, 1), (0, 4)],           # 3
]
# Edges (undirected, deduped): 0-1=1, 0-2=2, 0-3=4, 1-2=2, 2-3=1
```

## Why it works — the cut property

A **cut** splits the nodes into two groups: those *in* the tree and those *out*.
An edge **crosses** the cut if one endpoint is in and the other is out. The
foundation of Prim's correctness is the **cut property**:

> For any cut, the **lightest edge crossing it** is safe — it belongs to *some*
> MST.

Sketch of why: suppose the lightest crossing edge `e` (weight `w`) is *not* in
some MST `T`. Adding `e` to `T` creates a cycle, and that cycle must cross the cut
an even number of times — so it contains another crossing edge `f` with weight
`≥ w`. Swap: remove `f`, add `e`. The result is still a spanning tree, and its
total weight did not increase. So an MST containing `e` exists. ∎

Prim applies this repeatedly. The cut is always "{nodes in the tree} vs {the
rest}", and at every step we pick the lightest edge crossing *that* cut. Each pick
is safe, so the tree we build is an MST. The greedy local choice is globally
optimal precisely because of the cut property.

## Detailed walkthrough

Trace `prims(SAMPLE_UNDIRECTED)`. `add_node(x)` marks `in_mst[x]` and pushes all
of `x`'s edges to *not-yet-in-tree* neighbours. Heap shown as a sorted multiset
of `(weight, from, to)`.

Start: `add_node(0)` → `in_mst=[T,F,F,F]`,
`heap = {(1,0,1), (2,0,2), (4,0,3)}`, `mst = [[],[],[],[]]`.

| pop | `in_mst[to]`? | action | `mst` edges added | heap after |
|-----|---------------|--------|-------------------|------------|
| `(1,0,1)` | no | accept; `add_node(1)` pushes `(2,1,2)` | `0-1 (1)` | `{(2,0,2),(2,1,2),(4,0,3)}` |
| `(2,0,2)` | no | accept; `add_node(2)` pushes `(2,2,1)?`→1 in tree skip, `(1,2,3)` | `0-2 (2)` | `{(2,1,2),(1,2,3)?,(4,0,3)}` = `{(1,2,3),(2,1,2),(4,0,3)}` |
| `(1,2,3)` | no | accept; `add_node(3)` pushes `(4,3,0)?`→0 in tree skip | `2-3 (1)` | `{(2,1,2),(4,0,3)}` |
| `(2,1,2)` | **yes** (2 already in) | **skip stale** | — | `{(4,0,3)}` |
| `(4,0,3)` | **yes** (3 already in) | **skip stale** | — | `{}` |

Heap empty → done. Chosen edges: `0-1 (1)`, `0-2 (2)`, `2-3 (1)`. Total weight
`1 + 2 + 1 = 4` = `SAMPLE_UNDIRECTED_MST_WEIGHT`. That matches
`test_total_weight_is_minimal`.

Each accepted edge is recorded on **both** endpoints:

```python
mst[frm].append((to, weight))   # e.g. mst[0].append((1, 1))
mst[to].append((frm, weight))   # and  mst[1].append((0, 1))
```

So the result for this run is:

```python
mst = [
    [(1, 1), (2, 2)],   # 0
    [(0, 1)],           # 1
    [(0, 2), (3, 1)],   # 2
    [(2, 1)],           # 3
]
```

`test_returns_spanning_tree` checks via `is_connected_spanning_tree`: exactly
`n - 1 = 3` undirected edges, and all nodes reachable from 0. (Note: edge `1-2`
also has weight 2, so an MST using `1-2` instead of `0-2` is equally valid — the
test checks total weight and connectivity, not an exact edge set.)

The reference's loop, with the stale-skip guard:

```python
add_node(0)
while heap:
    weight, frm, to = heapq.heappop(heap)
    if in_mst[to]:        # stale: `to` joined the tree after this was pushed
        continue
    mst[frm].append((to, weight))
    mst[to].append((frm, weight))   # record on BOTH endpoints
    add_node(to)
```

## Complexity, derived

- **Time: `O(E log V)`.** Each undirected edge is pushed to the heap at most twice
  (once from each endpoint when that endpoint joins the tree), so `O(E)` pushes,
  each `O(log V)`. We pop `O(E)` entries, each `O(log V)`. Total `O(E log V)`.
- **Space: `O(V + E)`.** The heap holds up to `O(E)` candidate edges; `in_mst` is
  `O(V)`; the output `mst` holds the `V - 1` chosen edges twice = `O(V)`.

## Edge cases in detail

- **Empty graph** (`test_empty_graph_returns_none`): `prims([])` → `n == 0`, so
  the function returns **`None`** (not `[]`). This is the first line of the
  reference. An MST of zero nodes is undefined, hence `None`.
- **Stale heap entries.** As the trace shows, `(2,1,2)` and `(4,0,3)` are popped
  *after* their `to` endpoints already joined the tree. The `if in_mst[to]:
  continue` guard discards them. Without it you would add a redundant edge and
  create a cycle — no longer a tree.
- **Both endpoints recorded.** The validators (`collect_mst_edges`,
  `is_connected_spanning_tree`) traverse `mst` like a real undirected adjacency
  list. If you append to only `mst[frm]`, the graph is half-connected and
  `is_connected_spanning_tree` fails.
- **Ties.** When several crossing edges share the minimum weight (e.g. `0-2` and
  `1-2` both weigh 2), the heap's tuple ordering breaks the tie deterministically;
  any choice yields a valid MST of the same total weight.

## Variations & trade-offs

- **Prim vs Kruskal.** Kruskal sorts *all* edges once and adds the next-cheapest
  edge that does not form a cycle, using a **union-find** (disjoint-set) structure
  to detect cycles. Kruskal is `O(E log E)` and processes the whole edge list
  globally; Prim grows locally from a seed and shines on dense graphs (and with a
  Fibonacci heap reaches `O(E + V log V)`). Both rely on the cut property —
  Kruskal via the equivalent "every edge added is the lightest across *some*
  cut".
- **MST vs shortest-path tree — they differ!** Prim minimises *total* edge weight
  (no source); Dijkstra minimises *distance from a source* to each node. Same
  graph, different trees. Take the triangle `A-B=1, B-C=1, A-C=1.5`:
  - **MST** takes the two lightest edges `A-B` and `B-C` → total weight **2**.
  - **Shortest-path tree from A** takes `A-B (1)` and `A-C (1.5)`, because reaching
    `C` directly costs 1.5, beating the `A-B-C` route at 2.

  Different edge sets from one graph. Never use one when you need the other.
- **Disconnected graphs.** Prim from node 0 only spans 0's component. To span a
  forest you would restart from each unvisited node (the tests use connected
  graphs).

## Connections

- [`dijkstra.deep.md`](dijkstra.deep.md) — same heap-driven greedy shape; contrast
  what each minimises (crossing-edge weight vs cumulative distance) and why the
  trees differ.
- [`../heap/min_heap.md`](../heap/min_heap.md) — the priority queue that yields
  the cheapest crossing edge each step; a plain list here is `O(V·E)`.
- [`bfs_graph_matrix.deep.md`](bfs_graph_matrix.deep.md) /
  [`dfs_graph_list.deep.md`](dfs_graph_list.deep.md) — the unweighted traversals;
  Prim is what you reach for once edge weights and "connect everything cheaply"
  enter the picture.

## Self-check

1. State the cut property and explain, in one sentence, why it makes Prim's greedy
   choice safe.
2. Why must each accepted edge be appended to *both* `mst[frm]` and `mst[to]`?
   Which test fails if you do only one?
3. In the trace, `(2,1,2)` is popped but skipped. What would adding it have
   created, and which guard prevents that?
4. Why does `prims([])` return `None` rather than `[]`?
5. Give a concrete graph where the MST and the shortest-path tree from some source
   are different trees.
6. How does Kruskal detect cycles without growing from a seed, and what data
   structure does it use?

## Deep dive: common bugs

- **Adding an edge into a node already in the tree.** Re-check `in_mst[to]` *after*
  popping — the entry may have gone stale while it waited in the heap. Skipping
  this creates a cycle, so the result is no longer a tree (wrong MST).
- **Recording only one endpoint.** The MST is undirected; append to both
  `mst[frm]` and `mst[to]`, or `is_connected_spanning_tree` sees a broken graph.
- **Returning the total weight instead of the adjacency list.** The contract is
  the `mst` adjacency list (`WeightedAdjacencyList`), not a number.
- **Forgetting the empty-graph case.** `n == 0` must return `None`, not `[]` or an
  empty-but-non-None list.
- **Using a plain list as the priority queue.** Scanning for the minimum crossing
  edge each round is `O(E)` per step → `O(V·E)` overall. Use `heapq`.
- **Confusing Prim with Dijkstra.** Pushing `dist[from] + weight` (cumulative)
  instead of just `weight` turns Prim into something that builds a shortest-path
  tree, not an MST.
