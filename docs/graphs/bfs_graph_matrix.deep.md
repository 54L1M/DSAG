# BFS Path on a Weighted Adjacency Matrix — In Depth

> In-depth companion · graphs · stub: `src/topics/graphs/bfs_graph_matrix.py` · test: `tests/test_bfs_graph_matrix.py`
>
> New here? Read the [quick version](bfs_graph_matrix.md) first.

## The mental model

BFS is **ripples from a stone dropped in water**. Drop the stone at the source;
the first ring is every node one hop away, the next ring is every node two hops
away, and so on. Because you finish an entire ring before starting the next, the
*first time* you touch a node you have reached it in the **fewest possible hops**.

That single fact is the whole point: on an unweighted graph, BFS gives the
shortest path measured in *number of edges*. (Weights are ignored here — and in
this matrix every present edge is just a `1` anyway.)

Three pieces of bookkeeping:

- a **queue** (`collections.deque`) of nodes waiting to be expanded — FIFO is what
  makes the rings come out in order;
- `seen` — so a node enters the queue exactly once;
- `prev` — the node we *arrived from*. This is how we rebuild the path at the end;
  BFS does not carry the path around, it carries breadcrumbs.

The graph is a `WeightedAdjacencyMatrix` (`common/types.py`):

```python
WeightedAdjacencyMatrix = list[list[int]]   # matrix[from][to] == weight, 0 == no edge
```

The fixture `SAMPLE_MATRIX` as a picture:

```
   (0)
   / \          edges:  0 -> 1,  0 -> 2,  1 -> 3,  2 -> 3   (all directed)
  v   v
 (1) (2)
   \ /
    v
   (3)
```

and as the matrix (`row` = from, `col` = to, `0` = **no edge**):

```python
SAMPLE_MATRIX = [
    #  to: 0  1  2  3
    [ 0, 1, 1, 0 ],   # from 0 -> 1, 0 -> 2
    [ 0, 0, 0, 1 ],   # from 1 -> 3
    [ 0, 0, 0, 1 ],   # from 2 -> 3
    [ 0, 0, 0, 0 ],   # from 3 -> (nothing)
]
```

**Adjacency list vs matrix.** A matrix uses `O(V²)` space whether the graph is
sparse or dense, and to find node `curr`'s neighbours you must scan an entire row
of `V` cells, skipping the `0`s. A list uses `O(V + E)` and hands you the
neighbours directly. The matrix's payoff is `O(1)` "does edge `a -> b` exist?".
This exercise uses a matrix specifically so you feel the `O(V²)` row-scan cost.

## Why it works — the invariant

The contract: **return the fewest-edges path from `source` to `needle`, or
`None`**. BFS holds this invariant:

> Nodes are dequeued in non-decreasing order of their distance (hop count) from
> the source, and `prev[x]` records a parent that is exactly one hop closer.

Why it holds: the queue is FIFO and we enqueue a node only the *first* time we
see it (guarded by `seen`). The first time you reach a node is via a shortest
chain of `prev` links, because every earlier-dequeued node was at distance ≤ the
current one. So walking `prev` backwards from `needle` yields a shortest (fewest
edges) path. The reversal at the end just turns "needle → source" into
"source → needle".

This breaks the moment edges have *meaningful* weights — then "fewest edges" ≠
"least total weight", and you need Dijkstra. BFS only equals shortest-path when
every edge costs the same.

## Detailed walkthrough

Trace `bfs(SAMPLE_MATRIX, 0, 3)`. State: `queue`, `seen`, `prev` (`-1` = none).

Initial: `seen[0]=True`, `queue=[0]`, `prev=[-1,-1,-1,-1]`.

| step | dequeue | scan row → enqueue unseen edges | queue after | prev |
|------|---------|----------------------------------|-------------|------|
| 1 | `0` | col 1 (`=1`, unseen) → `prev[1]=0`; col 2 (`=1`, unseen) → `prev[2]=0`; cols 0,3 are `0` skip | `[1, 2]` | `[-1,0,0,-1]` |
| 2 | `1` | col 3 (`=1`, unseen) → `prev[3]=1`; rest `0` | `[2, 3]` | `[-1,0,0,1]` |
| 3 | `2` | col 3 is an edge but `seen[3]` → skip | `[3]` | unchanged |
| 4 | `3` | `curr == needle` → **break** | `[]` | unchanged |

Now reconstruct. Start at `needle = 3` and follow `prev` until `-1`:

```
at = 3   -> path = [3],       prev[3] = 1
at = 1   -> path = [3, 1],    prev[1] = 0
at = 0   -> path = [3, 1, 0], prev[0] = -1  (stop)
path.reverse() -> [0, 1, 3]
```

So `bfs` returns `[0, 1, 3]`. Note step 3: node `2` *also* has an edge into `3`,
but because `3` was already discovered via `1` (which was enqueued first), `2`'s
edge is ignored — BFS keeps the *first* (shortest) parent. Either `[0,1,3]` or
`[0,2,3]` would be a shortest path, and FIFO ordering picks the one through `1`.

The reference marks `seen` when it **enqueues**, not when it dequeues:

```python
for to in range(n):
    if graph[curr][to] == 0 or seen[to]:
        continue
    seen[to] = True          # mark on enqueue
    prev[to] = curr
    q.append(to)
```

## Complexity, derived

- **Time: `O(V²)`.** Each of the `V` nodes is dequeued at most once (thanks to
  `seen`). For each dequeued node we scan its full matrix *row* of `V` cells to
  find neighbours. `V` dequeues × `V` cells = `O(V²)`. The reconstruction walk is
  at most `O(V)`, dominated by the scan.
  *(With an adjacency list, the same algorithm is `O(V + E)` because you iterate
  only real edges — the `O(V²)` here is purely the matrix's row-scan tax.)*
- **Space: `O(V)`.** The queue, `seen`, and `prev` each hold at most `V` entries.

## Edge cases in detail

- **`source == needle`** (`test_source_equals_needle`): `bfs(SAMPLE_MATRIX, 2, 2)`.
  We mark `seen[2]`, enqueue `2`, dequeue it, and the `curr == needle` check
  breaks immediately. `seen[2]` is `True`, so we reconstruct: `at=2`,
  `prev[2]=-1`, giving `[2]`. Returns `[2]`.
- **Unreachable needle** (`test_unreachable_returns_none`):
  `bfs(SAMPLE_MATRIX, 3, 0)`. Node `3`'s row is all `0`, so nothing is enqueued;
  the queue drains. After the loop, `seen[0]` is still `False`, so we return
  `None`. No edge points *into* node `0`, so it is genuinely unreachable.
- **Matrix `0` is NOT a zero-cost edge.** The guard `graph[curr][to] == 0`
  treats `0` as *absence of an edge*. If you misread it as a weight, you would
  invent edges between every pair of nodes.
- **Exact-path assertion.** Unlike the DFS test, `test_finds_shortest_hop_path`
  asserts the *exact* list `[0, 1, 3]`. BFS can do this because its answer is
  deterministic given the row-scan order.

## Variations & trade-offs

- **List instead of matrix.** Swap the row scan for `for to, _w in graph[curr]`
  and the algorithm becomes `O(V + E)` — the standard BFS.
- **Distance instead of path.** Replace `prev` with a `dist` array
  (`dist[to] = dist[curr] + 1`); skip reconstruction. Useful for "how many hops?"
  questions.
- **Multi-source BFS.** Seed the queue with several sources at distance 0 (e.g.
  "nearest exit from any cell" in the maze exercise) — the rings still come out
  in order.
- **0-1 BFS.** If edges weigh only 0 or 1, a `deque` with `appendleft` for 0-edges
  gives shortest weighted paths in `O(V + E)` — a halfway house to Dijkstra.

## Connections

- [`dfs_graph_list.deep.md`](dfs_graph_list.deep.md) — the depth-first sibling;
  BFS finds the *fewest-edges* path, DFS finds *a* path.
- [`dijkstra.deep.md`](dijkstra.deep.md) — BFS generalised to weighted edges; a
  min-heap replaces the plain FIFO queue.
- [`../linear/queue.md`](../linear/queue.md) — the FIFO queue is what orders the
  rings; using a list with `pop(0)` instead makes BFS `O(V³)`.
- [`../trees/bt_bfs.md`](../trees/bt_bfs.md) — level-order tree traversal is BFS
  on a tree (no `seen` needed because trees have no cycles).

## Self-check

1. Why does the *first* time BFS reaches a node guarantee a fewest-edges path?
2. Why must you mark `seen[to] = True` when *enqueuing*, not when dequeuing? What
   goes wrong otherwise?
3. The reconstruction produces `[3, 1, 0]` before the reverse. Why is `prev`
   naturally backwards?
4. Why is this BFS `O(V²)` while a list-based BFS is `O(V + E)`?
5. In `SAMPLE_MATRIX`, both `[0,1,3]` and `[0,2,3]` are shortest. Why does the
   code return the one through `1`?
6. If `SAMPLE_MATRIX[1][3]` were `5` instead of `1`, would BFS still find a valid
   path? Would the path's *total weight* be minimal?

## Deep dive: common bugs

- **Treating matrix `0` as an edge.** `0` means *no edge*. Skip it with
  `if graph[curr][to] == 0: continue`. Otherwise you fabricate a complete graph.
- **Reconstructing forwards / forgetting to reverse.** Walking `prev` yields the
  path needle→source. You must `path.reverse()` (or build it reversed) — else you
  return `[3, 1, 0]` instead of `[0, 1, 3]`.
- **Marking `seen` on dequeue.** A node can then be enqueued by several parents
  before it is processed, inflating the queue and corrupting `prev`.
- **Using `list.pop(0)` as the queue.** `pop(0)` is `O(V)`, turning the loop into
  `O(V³)`. Use `collections.deque` and `popleft()`.
- **Forgetting the `None` case.** When `needle` is never `seen`, return `None`,
  not an empty or partial path.
