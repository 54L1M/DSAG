# Binary Tree Breadth-First (Level-order) Traversal

> trees · stub: `src/topics/trees/bt_bfs.py` · test: `tests/test_bt_bfs.py`
>
> 📚 Need more detail? See the [in-depth version](bt_bfs.deep.md).

## Intuition
Breadth-first search (BFS), also called level-order, visits the tree **one level
at a time, left to right**: the root, then all its children, then all their
children, and so on. Unlike the depth-first orders (pre/in/post) which dive deep
along one branch, BFS sweeps across. Picture reading a multi-story building floor
by floor instead of stairwell by stairwell. The tool that makes this work is a
**queue** (first-in, first-out): you always process the oldest node waiting in line.

## How it works
We use the given `BinaryNode` (fields: `value`, `left`, `right`) and a
`collections.deque` as the queue.

1. If `root` is `None`, return `[]` (empty tree).
2. Start the queue with `[root]`.
3. While the queue is not empty:
   - Pop the front node with `q.popleft()`.
   - Append its `value` to the output.
   - Enqueue `node.left` (if not `None`), then `node.right` (if not `None`).
4. Return the collected values.

Trace it on the fixture tree:

```
          20
        /    \
       10     50
      /  \   /  \
     5   15 30  100
```

- Queue `[20]` → pop 20, emit 20, enqueue 10, 50 → queue `[10, 50]`.
- Pop 10, emit 10, enqueue 5, 15 → queue `[50, 5, 15]`.
- Pop 50, emit 50, enqueue 30, 100 → queue `[5, 15, 30, 100]`.
- Pop the rest in order: emit 5, 15, 30, 100.

Output order: `[20, 10, 50, 5, 15, 30, 100]` — exactly the level-order shape.

## Complexity
- **Time:** O(n) — each node is enqueued and dequeued exactly once.
- **Space:** O(n) — the queue can hold a whole level; the widest level of a
  balanced tree is about n/2 nodes, so worst case is O(n).

The FIFO queue guarantees nodes leave in the order they were discovered: by level.

## Common pitfalls
- Using a plain `list` as a queue with `pop(0)` — that is O(n) per pop (it shifts
  every element). Use `collections.deque` and `popleft()` for O(1).
- Forgetting the empty-tree case → calling `popleft()` logic on `None`.
- Enqueuing children **without** the `is not None` check → `None` slips into the
  queue and crashes when you read its `.value`.
- Enqueuing right before left, which mirrors each level.
- Confusing BFS with DFS — BFS goes wide (queue), DFS goes deep (recursion/stack).

## Your task
Implement in `src/topics/trees/bt_bfs.py`, then run:

```bash
uv run pytest -k bt_bfs
```

Peek at `solutions/bt_bfs.py` only once you've given it a real attempt.
