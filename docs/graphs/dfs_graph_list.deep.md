# DFS Path on a Weighted Adjacency List — In Depth

> In-depth companion · graphs · stub: `src/topics/graphs/dfs_graph_list.py` · test: `tests/test_dfs_graph_list.py`
>
> New here? Read the [quick version](dfs_graph_list.md) first.

## The mental model

DFS is **wandering a maze with one hand on the wall**. You commit to a corridor
and keep going *deeper* until you either find the exit or hit a dead end. At a
dead end you walk back to the last junction you had an unexplored door and try
that one. You only ever back up when there is nothing new ahead.

Two pieces of bookkeeping make this work:

- `seen` — nodes you have already stepped on. Without it, a cycle like
  `0 -> 1 -> 0` traps you forever.
- `path` — the corridor you are *currently* standing in, from the source to where
  you are now. When you back up, you erase the last room from `path` (that is the
  **backtrack**).

The graph we walk is a `WeightedAdjacencyList` (see `common/types.py`):

```python
GraphEdge            = tuple[int, int]          # (destination, weight)
WeightedAdjacencyList = list[list[GraphEdge]]   # graph[node] -> edges leaving node
```

DFS ignores the weights entirely — it only cares *whether* an edge exists.

Here is the fixture `SAMPLE_LIST` as a picture (arrows are directed; weights on
edges):

```
        3        1
   (0) -----> (1) -----> (4)
    | \        |  \       | \
   1|  \3     4|   \1    1|  \5     2
    v   \      v    \     v   \     +--> (5) --1--> (6) --1--> (7)
   (2)<--      (2)   (3)<-(3)  (1)        ^                 (3),(5)
                                          |                  back to (6)
                                       (4)+--2
```

and as its real representation (index = node, value = list of `(to, weight)`):

```python
SAMPLE_LIST = [
    [(1, 3), (2, 1)],          # 0
    [(0, 3), (2, 4), (4, 1)],  # 1
    [(1, 4), (3, 7), (0, 1)],  # 2
    [(2, 7), (4, 5), (6, 1)],  # 3
    [(1, 1), (3, 5), (5, 2)],  # 4
    [(6, 1), (4, 2)],          # 5
    [(3, 1), (5, 1), (7, 1)],  # 6
    [(6, 1)],                  # 7
]
```

**Adjacency list vs matrix.** A list stores only the edges that exist, so it
costs `O(V + E)` space and lets you iterate a node's neighbours directly. A
matrix (used by the BFS exercise) costs `O(V²)` space but answers "is there an
edge `a -> b`?" in `O(1)`. Lists win for sparse graphs and neighbour scans;
matrices win for dense graphs and constant-time edge lookups.

## Why it works — the invariant

The contract is: **return *a* path from `source` to `needle`, or `None`**. DFS
guarantees correctness through one invariant:

> Every node in `path` is on the route from `source` to the node we are currently
> visiting, and no node appears twice.

`seen` enforces "no node twice", which guarantees **termination**: each node is
entered at most once, so the recursion cannot loop. `path` mirrors the recursion
stack — we `append` on the way down and `pop` on the way back up — so whenever we
*succeed* (`curr == needle`), `path` is exactly a valid walk from source to
needle, and we stop touching it. That is the answer.

What DFS does **not** guarantee is the *shortest* path. It returns the first
route it stumbles into, dictated by neighbour ordering. For shortest paths you
need BFS (fewest edges) or Dijkstra (least weight).

## Detailed walkthrough

Trace `dfs(SAMPLE_LIST, 0, 6)`. The reference solution recurses with a `_walk`
helper that returns `True` once the needle is found:

```python
def _walk(graph, curr, needle, seen, path):
    if seen[curr]:
        return False
    seen[curr] = True
    path.append(curr)
    if curr == needle:
        return True
    for to, _weight in graph[curr]:
        if _walk(graph, to, needle, seen, path):
            return True
    path.pop()        # dead end: backtrack
    return False
```

| step | call | action | `path` after |
|------|------|--------|--------------|
| 1 | `_walk(0)` | mark 0, append; not needle; try first edge `1` | `[0]` |
| 2 | `_walk(1)` | mark 1, append; try edges `0`(seen), `2` | `[0,1]` |
| 3 | `_walk(2)` | mark 2, append; try `1`(seen), `3` | `[0,1,2]` |
| 4 | `_walk(3)` | mark 3, append; try `2`(seen), `4` | `[0,1,2,3]` |
| 5 | `_walk(4)` | mark 4, append; try `1`(seen), `3`(seen), `5` | `[0,1,2,3,4]` |
| 6 | `_walk(5)` | mark 5, append; try `6` | `[0,1,2,3,4,5]` |
| 7 | `_walk(6)` | mark 6, append; `curr == needle` → **return True** | `[0,1,2,3,4,5,6]` |

Each `True` bubbles straight up the stack without popping, so `dfs` returns
`[0, 1, 2, 3, 4, 5, 6]`. Notice this is a perfectly valid path — but it is **not**
the shortest. Dijkstra finds `[0, 1, 4, 5, 6]` (weight 7); DFS found a longer one
because it dove into node `1`'s `(2, 4)` edge before reaching `(4, 1)` only after
backtracking would have been needed. DFS simply takes the first route the
neighbour order hands it.

To *see* a backtrack, imagine the needle were unreachable down a branch: step 6
would find node `5`'s neighbours all seen, `path.pop()` removes `5`, control
returns to `_walk(4)`, which tries its next neighbour. That pop is the
hand-off-the-wall moment.

## Complexity, derived

- **Time: `O(V + E)`.** The `seen` guard means each node's `_walk` body runs at
  most once → `O(V)` node work. Inside each, the `for to, _weight in graph[curr]`
  loop touches every outgoing edge once → summed over all nodes that is `O(E)`.
  Total `O(V + E)`.
- **Space: `O(V)`.** `seen` and `path` are each length `V`, and the recursion
  stack is at most `V` deep (a single chain visits every node once).

## Edge cases in detail

- **`source == needle`** (`test_source_equals_needle`): `_walk(3)` marks `3`,
  appends it, and the `curr == needle` check fires *immediately*, returning
  `[3]`. The crucial detail: you must `append` **before** the needle check, or
  this case returns an empty path. The reference does exactly that.
- **Unreachable needle** (`test_unreachable_returns_none`): graph
  `[[], [(0, 1)]]`, call `dfs(graph, 0, 1)`. Node `0` has no outgoing edges, so
  the `for` loop body never runs, `path.pop()` removes `0`, `_walk` returns
  `False`, and `dfs` returns `None`. The contract is `None` (not `[]`) when no
  route exists.
- **Valid-path test** (`test_finds_a_valid_path`): the test does not assert an
  *exact* path; it calls `is_valid_list_path`, which only checks the path starts
  at the source, ends at the needle, and every consecutive pair is a real edge.
  Any DFS route passes — that is by design, since DFS does not promise a unique
  answer.

## Variations & trade-offs

- **Recursive vs iterative.** The reference recurses. You can do the same with an
  explicit `stack` of nodes, but reconstructing the *path* (not just visiting) is
  fiddlier — you would track a `prev` array like BFS does, or push partial paths.
  Recursion gives you `path` and backtracking for free via the call stack.
- **Visited-on-enter vs visited-on-push.** DFS marks `seen` when it *enters* a
  node. That is correct here because we explore one branch at a time. (BFS marks
  on *enqueue* to avoid double-queueing — a different concern.)
- **All paths / longest path.** Remove the early `return True` and instead record
  `path[:]` (a copy) whenever `curr == needle`, then *always* backtrack. That
  enumerates every simple path — exponential in the worst case.
- **Cycle detection.** A three-colour DFS (white/grey/black) finds back-edges and
  thus cycles; useful for topological sorting.

## Connections

- [`bfs_graph_matrix.deep.md`](bfs_graph_matrix.deep.md) — the breadth-first
  sibling; contrast "dive deep" (stack/recursion) with "spread in rings"
  (queue), and *a* path vs the *fewest-edges* path.
- [`dijkstra.deep.md`](dijkstra.deep.md) — when edges have weights and you want
  the *cheapest* path, not just any path.
- [`../linear/stack.md`](../linear/stack.md) — DFS *is* a stack traversal; the
  recursion call stack is the implicit data structure.
- [`../trees/bt_bfs.md`](../trees/bt_bfs.md) — tree traversals are graph
  traversals on an acyclic graph where `seen` is unnecessary.

## Self-check

1. Why does DFS need a `seen` array but a tree traversal does not?
2. At exactly which line must `path.append(curr)` happen so that
   `source == needle` returns `[source]` rather than `[]`?
3. The DFS trace returned a 7-node path; Dijkstra returns a 5-node one. Did DFS
   make a mistake? Why or why not?
4. When does `path.pop()` execute, and what real-world action does it model?
5. If you reordered node `0`'s edges to `[(2, 1), (1, 3)]`, would `dfs(.., 0, 6)`
   still return a valid path? Would it return the *same* path?
6. How would you change the code to return *all* simple paths from source to
   needle instead of the first one?

## Deep dive: common bugs

- **Forgetting `seen` (or checking it too late).** A cycle sends recursion
  infinite and pytest times out. The guard `if seen[curr]: return False` must be
  the *first* thing `_walk` does.
- **Popping at the wrong time.** Calling `path.pop()` *before* recursing into
  neighbours corrupts the path; pop only *after* every neighbour has failed.
- **Returning `path` on failure.** When no route exists you must return `None`.
  Returning the (now-empty, post-backtrack) `path` returns `[]`, which is a
  different, wrong contract.
- **Marking `seen` after the needle check.** If you check `curr == needle` before
  appending to `path`, the `source == needle` case loses its node.
- **Confusing DFS with shortest path.** DFS returns *a* path. If a test asserted
  an exact shortest path, DFS would fail — reach for BFS or Dijkstra instead.
