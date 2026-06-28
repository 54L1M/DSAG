# Binary Tree In-order Traversal

> trees · stub: `src/topics/trees/bt_in_order.py` · test: `tests/test_bt_in_order.py`
>
> 📚 Need more detail? See the [in-depth version](bt_in_order.deep.md).

## Intuition
In-order means: **visit the left subtree first, then the node, then the right
subtree** ("in" = the node is handled *in between* its children). The magic
property: for a **binary search tree** (where left < node < right), in-order
traversal yields the values in **sorted ascending order**. Imagine pages numbered
left-to-right in a book — read everything to the left of a page, then the page,
then everything to its right, and the numbers come out in order.

## How it works
We use the given `BinaryNode` (fields: `value`, `left`, `right`) with a recursive
helper that appends into a shared `out` list.

1. If the current node is `None`, return (base case).
2. Recurse into `node.left` first.
3. Append `node.value`. **(visit the node, after the whole left side)**
4. Recurse into `node.right`.

Trace it on the fixture BST:

```
          20
        /    \
       10     50
      /  \   /  \
     5   15 30  100
```

- From 20, go all the way left: 10, then 5.
- 5 has no left → emit 5. Back to 10 → emit 10. 10's right is 15 → emit 15.
- Back to 20 → emit 20. Go right to 50: left child 30 → emit 30, emit 50,
  right child 100 → emit 100.

Output order: `[5, 10, 15, 20, 30, 50, 100]` — note it is **sorted**, which is the
whole point of the `test_sample_tree_is_sorted` test.

## Complexity
- **Time:** O(n) — every node is visited exactly once.
- **Space:** O(h) — recursion stack depth equals the tree height `h`
  (O(log n) balanced, O(n) worst case for a degenerate chain).

Each node is emitted once; extra memory is just the call stack along one path.

## Common pitfalls
- Forgetting the `None` base case → crash on a missing child.
- Appending the value **before** recursing left turns this into pre-order.
- Appending **after** both recursions turns it into post-order.
- Assuming the output is sorted for *any* tree — that only holds for a valid BST.
- Returning the node objects rather than `node.value`.

## Your task
Implement in `src/topics/trees/bt_in_order.py`, then run:

```bash
uv run pytest -k bt_in_order
```

Peek at `solutions/bt_in_order.py` only once you've given it a real attempt.
