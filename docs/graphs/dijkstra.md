# Dijkstra's Shortest Path

> graphs · stub: `src/topics/graphs/dijkstra.py` · test: `tests/test_dijkstra.py`
>
> 📚 Need more detail? See the [in-depth version](dijkstra.deep.md).

## Intuition
Dijkstra's algorithm finds the **cheapest** path in a graph with non-negative
edge weights. The greedy idea: always settle the **nearest unvisited node**
next. Like exploring a city by always walking to whichever reachable corner has
the smallest known travel time so far, you can be sure that once you "settle" a
node, you have already found its shortest distance — no later detour can beat it
(because all weights are non-negative). A min-heap keeps "who is nearest" fast.

## How it works
The graph is a `WeightedAdjacencyList`: `graph[n]` is a list of `(to, weight)`
edges. Using the fixture `SAMPLE_LIST`, node `0` has `[(1, 3), (2, 1)]`. We keep
a `dist` array (best known distance from the source, all starting at infinity)
and a `prev` array (predecessor on the best path). Steps for
`dijkstra(SAMPLE_LIST, 0, 6)`:

1. Set `dist[0] = 0` and push `(0, 0)` — that is `(distance, node)` — onto the
   heap.
2. **Pop the smallest** `(d, curr)`. If `curr` is already visited, skip this
   stale entry; otherwise mark it visited.
3. If `curr == sink`, stop early — its shortest distance is final.
4. **Relax** each edge `(to, weight)`: compute `nd = d + weight`. If `nd <
   dist[to]`, we found a cheaper route, so update `dist[to] = nd`,
   `prev[to] = curr`, and push `(nd, to)` onto the heap.
5. Repeat until the heap empties or the sink is settled.

For `SAMPLE_LIST` this settles the route `0 -> 1 -> 4 -> 5 -> 6` with total
weight **7** — cheaper than more direct-looking routes. To build the answer,
walk `prev` backwards from `sink` to `source` and **reverse** it.

Edge cases: if `source == sink`, the path is just `[source]`. If `sink` is
unreachable (`dist[sink]` stays infinity), return `[]`.

## Complexity
- **Time:** O((V + E) log V)
- **Space:** O(V)

Every edge can trigger one heap push, and each push/pop costs O(log V); the
`dist`, `prev`, and `visited` arrays are each O(V).

## Common pitfalls
- Pushing **stale entries** onto the heap (a node can appear multiple times with
  different distances) — filter them by skipping any popped node already marked
  visited.
- Forgetting `dist[source] = 0` before starting, so nothing ever relaxes.
- Returning the **distance** instead of the **path** — the contract wants the
  list of nodes.
- Mixing up the unreachable return value: this function returns `[]` (an empty
  list), not `None`.
- Using Dijkstra with **negative** weights — it can settle a node too early and
  give wrong answers.

## Your task
Implement in `src/topics/graphs/dijkstra.py`, then run:

```bash
uv run pytest -k dijkstra
```

Peek at `solutions/dijkstra.py` only once you've given it a real attempt.
