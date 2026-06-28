# BFS Path on a Weighted Adjacency Matrix

> graphs · stub: `src/topics/graphs/bfs_graph_matrix.py` · test: `tests/test_bfs_graph_matrix.py`
>
> 📚 Need more detail? See the [in-depth version](bfs_graph_matrix.deep.md).

## Intuition
Breadth-first search (BFS) explores in **rings**: first all nodes one step from
the source, then all nodes two steps away, and so on — like ripples spreading
out from a stone dropped in water. Because it reaches nearer nodes before farther
ones, BFS finds a path with the **fewest edges**. Where DFS dives deep with
recursion, BFS spreads wide using a queue.

## How it works
The graph is a `WeightedAdjacencyMatrix`: `graph[from][to]` is the edge weight,
and `0` means **no edge**. Using the fixture `SAMPLE_MATRIX`:

```
     to: 0  1  2  3
from 0 [ 0, 1, 1, 0 ]   # 0 -> 1, 0 -> 2
     1 [ 0, 0, 0, 1 ]   # 1 -> 3
     2 [ 0, 0, 0, 1 ]   # 2 -> 3
     3 [ 0, 0, 0, 0 ]   # no edges out
```

We use a queue, a `seen` array, and a `prev` array that records, for each node,
which node we arrived **from**. Steps for `bfs(SAMPLE_MATRIX, 0, 3)`:

1. Mark `seen[0] = True`, push `0` onto the queue.
2. Dequeue `0`. Scan row `graph[0]`: column `1` is `1` (an edge) and unseen →
   set `seen[1] = True`, `prev[1] = 0`, enqueue `1`. Same for column `2` →
   `prev[2] = 0`. Columns `0` and `3` are `0`, so skip them.
3. Dequeue `1`. Row `graph[1]` has an edge to `3` → `prev[3] = 1`, enqueue `3`.
4. Dequeue `2`. Its only edge is to `3`, but `3` is already seen → skip.
5. Dequeue `3` — that is the needle, stop.

Now **reconstruct backwards** using `prev`: start at `3`, follow
`prev[3] = 1`, `prev[1] = 0`, `prev[0] = -1` (stop). That yields `[3, 1, 0]`;
**reverse** it to get `[0, 1, 3]`. If `needle` was never seen, return `None`.

## Complexity
- **Time:** O(V^2)
- **Space:** O(V)

A matrix forces scanning all V columns for each of the V dequeued nodes, so V*V
work; the queue, `seen`, and `prev` arrays each hold at most V entries.

## Common pitfalls
- Treating weight `0` as a real edge — in this representation `0` means *no
  edge*, so always skip it.
- Reconstructing the path in the wrong direction (or forgetting to reverse it) →
  you return `[3, 1, 0]` instead of `[0, 1, 3]`.
- Marking a node `seen` when you *dequeue* it instead of when you *enqueue* it →
  the same node can get queued multiple times.
- Using a list and `pop(0)` instead of `collections.deque` — `pop(0)` is O(V)
  and turns BFS into O(V^3).
- Returning the path but forgetting the `None` case when `needle` is unreachable.

## Your task
Implement in `src/topics/graphs/bfs_graph_matrix.py`, then run:

```bash
uv run pytest -k bfs_graph_matrix
```

Peek at `solutions/bfs_graph_matrix.py` only once you've given it a real attempt.
