# Binary Tree Post-order Traversal

> trees · stub: `src/topics/trees/bt_post_order.py` · test: `tests/test_bt_post_order.py`
>
> 📚 Need more detail? See the [in-depth version](bt_post_order.deep.md).

## Intuition
Post-order means: **visit the left subtree, then the right subtree, then the node
last** ("post" = the node is handled *after* its children). Think of deleting a
file tree from disk: you must remove everything inside a folder before you can
delete the folder itself. Post-order is the order for any "compute children first,
then combine into the parent" job (sizes, sums, freeing memory).

## How it works
We use the given `BinaryNode` (fields: `value`, `left`, `right`) with a recursive
helper that appends into a shared `out` list.

1. If the current node is `None`, return (base case).
2. Recurse into `node.left`.
3. Recurse into `node.right`.
4. Append `node.value`. **(visit the node, only after both children are done)**

Trace it on the fixture tree:

```
          20
        /    \
       10     50
      /  \   /  \
     5   15 30  100
```

- Down the left of 10: emit 5, then 15, then 10 (parent after its kids).
- Down the right of 50: emit 30, then 100, then 50.
- Finally emit the root 20 (everything below it is finished).

Output order: `[5, 15, 10, 30, 100, 50, 20]` — the root always comes **last**.

## Complexity
- **Time:** O(n) — every node is visited exactly once.
- **Space:** O(h) — recursion stack depth equals the tree height `h`
  (O(log n) balanced, O(n) for a degenerate chain).

Single pass over nodes; only the call stack along one path uses extra memory.

## Common pitfalls
- Forgetting the `None` base case → crash on a missing child.
- Appending the value too early (before both recursions) gives pre- or in-order.
- Swapping the left/right recursion order flips the result.
- Expecting the root first — in post-order the root is the **last** element.
- Returning node objects instead of `node.value`.

## Your task
Implement in `src/topics/trees/bt_post_order.py`, then run:

```bash
uv run pytest -k bt_post_order
```

Peek at `solutions/bt_post_order.py` only once you've given it a real attempt.
