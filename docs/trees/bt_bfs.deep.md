# Binary Tree Breadth-First (Level-order) Traversal — In Depth

> In-depth companion · trees · stub: `src/topics/trees/bt_bfs.py` · test: `tests/test_bt_bfs.py`
>
> New here? Read the [quick version](bt_bfs.md) first.

## The mental model

The depth-first traversals dive down one branch as far as they can before backing
up. **Breadth-first search (BFS)**, also called **level-order**, does the opposite:
it sweeps the tree **level by level, left to right**. Root first, then both of the
root's children, then all of *their* children, and so on.

The tool that makes "oldest-discovered first" happen is a **queue** (first-in,
first-out). You always process the node that has been waiting longest, and when you
process it you add its children to the back of the line. Picture reading a building
floor by floor instead of taking one stairwell to the top.

Fixture tree (`SAMPLE_TREE_LEVEL_ORDER = [20, 10, 50, 5, 15, 30, 100]`):

```
          20            <- level 0
        /    \
       10     50        <- level 1
      /  \    /  \
     5   15  30  100    <- level 2
```

`bfs(root)` returns `[20, 10, 50, 5, 15, 30, 100]` — exactly the level-order
listing. (And, satisfyingly, exactly the list the fixture was built from — that is
how `build_tree` lays nodes out.)

## Why it works — the invariant

The queue maintains this **invariant**: *at all times the queue holds the
not-yet-processed nodes in non-decreasing order of depth, and within a depth, left
to right.* 

It holds initially (just the root, depth 0). It is preserved by each step: we
remove the front node — the shallowest, leftmost waiting node — and append its left
then right children to the back. Those children are exactly one level deeper than
their parent, and because we process parents in level order, their children are
enqueued in level order too. FIFO guarantees we never serve a deeper node before a
shallower one that is still waiting. Therefore nodes leave the queue (and get
emitted) in level order. That is the whole proof.

## Detailed walkthrough

```python
from collections import deque

def bfs(root):
    out = []
    if root is None:
        return out
    q = deque([root])
    while q:
        node = q.popleft()           # serve the front (oldest)
        out.append(node.value)
        if node.left is not None:
            q.append(node.left)      # children join the back
        if node.right is not None:
            q.append(node.right)
    return out
```

Trace, showing the queue (front on the left) before each pop and what gets emitted:

```
q=[20]                 pop 20  emit 20   enqueue 10,50
q=[10,50]              pop 10  emit 10   enqueue 5,15
q=[50,5,15]            pop 50  emit 50   enqueue 30,100
q=[5,15,30,100]        pop 5   emit 5    (no children)
q=[15,30,100]          pop 15  emit 15
q=[30,100]             pop 30  emit 30
q=[100]                pop 100 emit 100
q=[]                   stop
```

Final: `[20, 10, 50, 5, 15, 30, 100]`. See how level 1 (`10,50`) is fully emitted
before any of level 2, because the children we enqueue always land *behind* the
nodes already waiting.

## BFS vs. the DFS recursion

| | DFS (pre/in/post) | BFS (level-order) |
|---|---|---|
| Direction | deep along one branch | wide across a level |
| Bookkeeping | call **stack** (LIFO) | explicit **queue** (FIFO) |
| Implementation | naturally recursive | naturally iterative loop |
| Auxiliary space | **O(h)** (one path) | **O(n)** (one whole level) |

DFS rides the call stack, which only ever holds one root-to-node *path* (height
`h`). BFS must hold an entire *level* at once. That difference drives the space
analysis below.

## Complexity, derived

- **Time: O(n).** Each node is enqueued exactly once and dequeued exactly once;
  each operation is O(1) (see the deque note), so total work is proportional to `n`.
- **Space: O(n).** The queue's high-water mark is the **widest level**. In a
  balanced binary tree the bottom level holds up to about `n/2` nodes — half the
  tree is alive in the queue at once — so the bound is O(n). Contrast DFS's O(h):
  for a balanced tree that is O(log n) vs O(n), a real difference.

### Why `deque`, not a list

It is tempting to use a plain list with `q.pop(0)` to remove the front. **Don't.**
`list.pop(0)` is **O(n)**: removing index 0 forces Python to shift every remaining
element down one slot. Do that once per node and BFS degrades to **O(n²)** —
enough to time out on large trees. `collections.deque.popleft()` is **O(1)**: a
deque is a doubly-linked block structure with cheap removal at *both* ends. Always
reach for `deque` when you need a FIFO queue.

## Edge cases in detail

- **Empty tree.** `test_empty`: the `if root is None: return []` guard fires before
  we ever touch the queue. Without it, `deque([None])` would later try
  `None.value` and crash.
- **Single node.** `bfs(build_tree([42]))` → enqueue 42, pop it, no children → `[42]`.
- **Unbalanced / right-leaning chain.** `test_unbalanced` uses level-order
  `[1, None, 2, None, 3]`:

  ```
     1
      \
       2
        \
         3
  ```

  The queue never holds more than one node at a time (each node has a single child),
  so BFS emits `[1, 2, 3]`. This is the *cheapest* case for BFS space (O(1) live) —
  the mirror image of where DFS is most expensive (O(n) stack depth).

## Variations & trade-offs

- **Grouping by level.** To return a list-of-levels (e.g. `[[20], [10,50],
  [5,15,30,100]]`), snapshot `len(q)` at the top of each outer iteration and pop
  exactly that many — everyone currently in the queue is one level:

  ```python
  while q:
      level = []
      for _ in range(len(q)):     # exactly this level's nodes
          node = q.popleft()
          level.append(node.value)
          if node.left:  q.append(node.left)
          if node.right: q.append(node.right)
      levels.append(level)
  ```

- **DFS that knows its depth.** You *can* produce level groupings with DFS by
  passing a `depth` parameter and indexing into a list of lists — but plain
  flat level-order is far more natural with a queue.
- **When BFS is the right tool:** anything "per level" (level sums, right-side view,
  zig-zag order), and — crucially — **shortest path in an unweighted graph/tree**,
  because the first time BFS reaches a node it has reached it by the fewest edges.

## Connections

- The queue is the star — read [`../linear/queue.md`](../linear/queue.md) for why
  `deque` gives O(1) at both ends.
- DFS counterparts: [pre-order](bt_pre_order.deep.md), [in-order](bt_in_order.deep.md),
  [post-order](bt_post_order.deep.md).
- The *same* BFS pattern on a graph (with a visited set to avoid cycles):
  [`../graphs/bfs_graph_matrix.md`](../graphs/bfs_graph_matrix.md). DFS on graphs:
  [`../graphs/dfs_graph_list.md`](../graphs/dfs_graph_list.md). Iterative DFS uses a
  stack: [`../linear/stack.md`](../linear/stack.md).

## Self-check

1. Which data structure gives BFS its level-by-level order, and what property of it
   matters?
2. Why is BFS auxiliary space O(n) while DFS is O(h)? Where does the n/2 come from?
3. Why is `list.pop(0)` a trap, and what does it do to the overall complexity?
4. On the chain `1 -> 2 -> 3`, how many nodes are in the queue at the busiest moment?
   Compare to DFS's stack depth on the same tree.
5. How do you modify the loop to return nodes grouped by level?
6. Why is BFS the natural choice for shortest path in an *unweighted* graph?

## Deep dive: common bugs

- **Using a list as a queue** (`pop(0)`). Correct output, but O(n) per pop → O(n²)
  overall and possible timeouts. Use `deque.popleft()`.
- **Missing the empty-tree guard.** Seeding the queue with `None` (or skipping the
  early return) leads to `None.value` → `AttributeError`.
- **Enqueuing children without the `is not None` check.** A `None` slips into the
  queue and crashes when later popped and read.
- **Enqueuing right before left.** Mirrors every level → `[20, 50, 10, ...]`; fails
  the exact-list test.
- **Confusing BFS with DFS.** BFS = queue + iteration (wide); DFS = stack/recursion
  (deep). Reaching for recursion here quietly gives you a depth-first order instead.
