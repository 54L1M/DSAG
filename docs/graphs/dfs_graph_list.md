# DFS Path on a Weighted Adjacency List

> graphs · stub: `src/topics/graphs/dfs_graph_list.py` · test: `tests/test_dfs_graph_list.py`
>
> 📚 Need more detail? See the [in-depth version](dfs_graph_list.deep.md).

## Intuition
Depth-first search (DFS) explores like wandering a maze while always hugging one
wall: you commit to a path, go as **deep** as you can, and only when you hit a
dead end do you **backtrack** to the last fork and try a different branch. Unlike
BFS (which fans out in rings), DFS dives down one route fully before considering
alternatives. Any path it finds is valid, but it is not guaranteed to be the
shortest.

## How it works
The graph is a `WeightedAdjacencyList`: `graph[n]` is a list of `(to, weight)`
edges leaving node `n`. We ignore the weights here — DFS only cares about
connectivity. Using the fixture `SAMPLE_LIST`, node `0` has edges
`[(1, 3), (2, 1)]`, meaning `0 -> 1` and `0 -> 2`.

We recurse, carrying a `seen` array (so we never revisit a node) and a `path`
list (the route built so far). Steps for `dfs(SAMPLE_LIST, 0, 6)`:

1. Enter node `0`. It is not in `seen`, so mark `seen[0] = True` and append `0`
   to `path` → `[0]`.
2. `0` is not the needle. Try its first neighbour, `1`. Recurse.
3. At `1`, mark and append → `[0, 1]`. Try `1`'s neighbours: `0` (already seen,
   skip), `2`, then `4`...
4. Keep diving until we either reach node `6` (the needle) or dead-end.
5. **On success**: the current node equals `needle`, so return `True`. The `path`
   list already holds a valid route and bubbles back up untouched.
6. **On dead end**: every neighbour is seen or fails, so `path.pop()` removes the
   current node (backtrack) and we return `False` to the caller.

If the top-level call returns `True`, return `path`; otherwise return `None`.

## Complexity
- **Time:** O(V + E)
- **Space:** O(V)

Each node is visited at most once and each edge is examined once; the `seen`
array, recursion stack, and `path` are all bounded by the number of nodes V.

## Common pitfalls
- Forgetting `seen` (or checking it too late) → cycles like `0 -> 1 -> 0` send
  you into infinite recursion.
- Popping from `path` at the wrong time: only pop **after** all neighbours of a
  node have failed, not before recursing.
- Returning `path` even on failure — the contract wants `None` when no route
  exists.
- Treating this like a shortest-path search; DFS returns *a* path, not the
  cheapest one (use Dijkstra for that).
- Mutating `path` but forgetting to mark `seen[curr]` before the needle check,
  so the source-equals-needle case misbehaves.

## Your task
Implement in `src/topics/graphs/dfs_graph_list.py`, then run:

```bash
uv run pytest -k dfs_graph_list
```

Peek at `solutions/dfs_graph_list.py` only once you've given it a real attempt.
