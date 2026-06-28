# Dijkstra's Shortest Path — In Depth

> In-depth companion · graphs · stub: `src/topics/graphs/dijkstra.py` · test: `tests/test_dijkstra.py`
>
> New here? Read the [quick version](dijkstra.md) first.

## The mental model

BFS finds the path with the *fewest edges*. But edges often have **costs** — road
lengths, latencies, prices — and the route with fewest hops can be the most
expensive. Dijkstra finds the **cheapest** path when every edge weight is
non-negative.

The picture: you are exploring a city and you keep a list of "best travel time
discovered so far" to every corner. Repeatedly, you walk to whichever
**unvisited corner has the smallest known time**, declare its time *final*, and
update its neighbours. The trick that makes this fast is a **min-heap** (priority
queue) that always hands you the nearest unvisited node next.

Bookkeeping:

- `dist[node]` — best known distance from source (starts at `inf`, `dist[source]=0`).
- `prev[node]` — predecessor on the best path (for reconstruction, like BFS).
- `visited[node]` — once `True`, the node is *finalized*; we never revisit it.
- a min-heap of `(distance, node)` pairs.

The graph is a `WeightedAdjacencyList`:

```python
WeightedAdjacencyList = list[list[tuple[int, int]]]   # graph[n] -> [(to, weight), ...]
```

Fixture `SAMPLE_LIST` (directed) as a picture, with weights:

```
        3         1         2         1
   (0) ---> (1) ---> (4) ---> (5) ---> (6) ---> (7)
    |        |        |        ^        | \
   1|       4|       5|       2|       1|  \1
    v        v        v        |        v   +-> (3) -1-> (6)
   (2) <-1- ... (3) <--------- + ...   (3)
```

(The full edge set is below; the picture highlights the winning route.)

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

## Why it works — the invariant

The greedy invariant:

> When a node is **popped from the heap and marked visited**, `dist[node]` is its
> true shortest distance from the source — no future discovery can lower it.

Why? When we pop node `u` with distance `d`, every *other* node still in the heap
has distance ≥ `d` (the heap pops the minimum). Any alternative path to `u` must
go through some not-yet-finalized node `w`, and since all edge weights are
**non-negative**, that path costs at least `dist[w] ≥ d`. So no detour can beat
`d`. Therefore `d` is final.

**This is exactly why negative weights break Dijkstra.** With a negative edge, a
"longer" route through a not-yet-visited node could later *subtract* weight and
undercut a node we already finalized — but we have already locked it in and moved
on. The proof "all remaining paths cost ≥ d" collapses. (For negative edges use
Bellman–Ford.)

**Relaxation** is the update step: for edge `u -> v` of weight `w`, if
`dist[u] + w < dist[v]`, we have found a cheaper way to `v`, so we lower
`dist[v]`, set `prev[v] = u`, and push the new `(dist[v], v)` onto the heap.

## Detailed walkthrough

Trace `dijkstra(SAMPLE_LIST, 0, 6)`. Heap shown as a sorted multiset of
`(dist, node)`; `dist` array indexed `0..7`; `∞` = `math.inf`.

Start: `dist = [0,∞,∞,∞,∞,∞,∞,∞]`, `heap = {(0,0)}`.

| pop | finalize | relax (edges that improve) | dist after | heap after |
|-----|----------|----------------------------|------------|------------|
| `(0,0)` | 0 | `1`: 0+3=3; `2`: 0+1=1 | `[0,3,1,∞,∞,∞,∞,∞]` | `{(1,2),(3,1)}` |
| `(1,2)` | 2 | `1`: 1+4=5 ≥ 3 no; `3`: 1+7=8; `0` visited | `[0,3,1,8,∞,∞,∞,∞]` | `{(3,1),(8,3)}` |
| `(3,1)` | 1 | `2` visited; `4`: 3+1=4 | `[0,3,1,8,4,∞,∞,∞]` | `{(4,4),(8,3)}` |
| `(4,4)` | 4 | `1` visited; `3`: 4+5=9 ≥ 8 no; `5`: 4+2=6 | `[0,3,1,8,4,6,∞,∞]` | `{(6,5),(8,3)}` |
| `(6,5)` | 5 | `6`: 6+1=7; `4` visited | `[0,3,1,8,4,6,7,∞]` | `{(7,6),(8,3)}` |
| `(7,6)` | 6 | `curr == sink` → **break** | — | — |

`dist[6] = 7`. Reconstruct via `prev`: `prev[6]=5`, `prev[5]=4`, `prev[4]=1`,
`prev[1]=0`. Walking back: `[6,5,4,1,0]`, reversed → `[0, 1, 4, 5, 6]`, total
weight **7** — exactly what `test_shortest_path` asserts.

Notice the heap *could* still hold `(8,3)`, a stale, never-needed entry. It never
matters because we break at the sink; even without the break, popping it later
would find node `3` either already visited or with `dist[3] ≤ 8` and the
`if visited[curr]: continue` / relaxation checks would discard it.

The reference's core loop:

```python
while heap:
    d, curr = heapq.heappop(heap)
    if visited[curr]:          # lazy deletion: skip stale entries
        continue
    visited[curr] = True
    if curr == sink:
        break
    for to, weight in graph[curr]:
        if visited[to]:
            continue
        nd = d + weight
        if nd < dist[to]:      # relaxation
            dist[to] = nd
            prev[to] = curr
            heapq.heappush(heap, (nd, to))
```

## The lazy-deletion heap pattern

Python's `heapq` has no "decrease-key" operation. So instead of *updating* a
node's entry when we relax it, we **push a fresh duplicate** with the smaller
distance. The heap now contains several entries for the same node. We make this
correct with one guard: when we pop a node, if it is already `visited` we
**skip** it (a stale entry — a better one was popped earlier). This is "lazy
deletion": stale entries linger but are harmless because the smallest (correct)
copy always pops first and finalizes the node.

The cost is a slightly bigger heap (up to `O(E)` entries) but the same
`O(log V)`-per-op asymptotics. It is far simpler than maintaining an indexed heap
with decrease-key.

## Complexity, derived

- **Time: `O((V + E) log V)`.** Each edge can trigger at most one push
  (relaxation), so the heap holds `O(E)` entries; each push/pop is `O(log E) =
  O(log V)` (since `E ≤ V²`, `log E = O(log V)`). We pop `O(V + E)` times total →
  `O((V + E) log V)`.
- **Space: `O(V + E)`.** `dist`, `prev`, `visited` are `O(V)`; the heap can hold
  `O(E)` pending entries.

## Edge cases in detail

- **`source == sink`** (`test_source_equals_sink`): `dijkstra(SAMPLE_LIST, 4, 4)`.
  `dist[4]=0`, push `(0,4)`. Pop it, mark visited, `curr == sink` → break.
  `dist[4] = 0 ≠ inf`, reconstruct: `prev[4]=-1` → `[4]`. Returns `[4]`.
- **Unreachable sink** (`test_unreachable_returns_empty`): graph
  `[[(1,1)], [(0,1)], []]`, call `dijkstra(graph, 0, 2)`. Node `2` has no
  incoming edges; the heap drains without ever lowering `dist[2]`. After the loop
  `dist[2] == math.inf`, so we return **`[]`** (an empty list). Contrast with
  DFS/BFS, which return `None`.
- **Cheaper-but-longer route** (`test_prefers_cheaper_longer_route`): graph
  `[[(1,10),(2,1)], [(0,10),(2,1)], [(0,1),(1,1)]]`, call `dijkstra(graph, 0, 1)`.
  The *direct* edge `0 -> 1` costs **10**. But `0 -> 2` (1) then `2 -> 1` (1)
  costs **2**. Trace: pop `(0,0)`, relax `1`→10, `2`→1. Pop `(1,2)` (the heap's
  minimum, not the direct route!), relax `1`: 1+1=2 < 10 → `dist[1]=2`,
  `prev[1]=2`. Pop `(2,1)`, `curr == sink`, break. Path `[0, 2, 1]`. Dijkstra
  correctly prefers the cheaper two-hop route over the expensive one-hop edge —
  the whole reason BFS is not enough on weighted graphs.

## Variations & trade-offs

- **No early break.** Dropping `if curr == sink: break` computes shortest paths
  to *all* nodes (single-source shortest paths) at the same asymptotic cost.
- **Negative edges → Bellman–Ford** (`O(V·E)`), which also detects negative
  cycles. Dijkstra cannot handle them, as shown above.
- **A\*.** Add a heuristic to the priority (`dist + heuristic(node, goal)`) to
  steer the search toward the goal — Dijkstra is A\* with a zero heuristic.
- **Dense graphs.** An array-based Dijkstra (scan for the min each round) is
  `O(V²)`, which beats the heap version when `E ≈ V²`.

## Connections

- [`bfs_graph_matrix.deep.md`](bfs_graph_matrix.deep.md) — Dijkstra *is* BFS with
  a priority queue instead of a FIFO; on a graph where all weights are equal they
  give the same answer.
- [`prim.deep.md`](prim.deep.md) — same heap-driven greedy *shape*, but Prim
  minimises the edge that connects a new node (MST), while Dijkstra minimises
  total distance from the source. Their trees differ!
- [`../heap/min_heap.md`](../heap/min_heap.md) — the priority queue powering the
  whole algorithm; understanding `heapq` push/pop is prerequisite.
- [`dfs_graph_list.deep.md`](dfs_graph_list.deep.md) — for *a* path with no
  weights, DFS suffices; Dijkstra is overkill there.

## Self-check

1. State the greedy invariant precisely. At what exact moment is a node's
   distance "finalized"?
2. Give a tiny graph with one negative edge where Dijkstra returns a wrong
   answer, and explain which step of the proof fails.
3. Why can the heap contain several entries for the same node, and what single
   line keeps that correct?
4. In `test_prefers_cheaper_longer_route`, why does `(1,2)` pop before the entry
   that would finalize node `1` directly?
5. Why does this function return `[]` for an unreachable sink while BFS returns
   `None`? Is that a meaningful difference or just convention?
6. If you removed the `if curr == sink: break`, what would the function still
   compute correctly, and what would change in cost?

## Deep dive: common bugs

- **Not skipping stale heap entries.** Without `if visited[curr]: continue`, you
  re-process nodes with outdated distances — wrong answers and wasted work.
- **Using a plain list as a priority queue.** Scanning a list for the min each
  step is `O(V)` per pop; use `heapq`. A list with `min()`/`remove()` is both
  slow and bug-prone.
- **Returning the distance instead of the path.** The contract wants the *list of
  nodes*. Returning `dist[sink]` is a classic mix-up (and vice versa for tasks
  that want the distance).
- **Wrong unreachable value.** This function returns `[]` (not `None`) when
  `dist[sink]` stays `inf`. Check `dist[sink] == math.inf` explicitly.
- **Forgetting `dist[source] = 0`.** Then the first pop never relaxes anything and
  every node looks unreachable.
- **Allowing negative weights.** Even one negative edge can violate the invariant
  and silently produce a wrong path — switch to Bellman–Ford.
