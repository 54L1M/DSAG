# Binary Tree Pre-order Traversal

> trees · stub: `src/topics/trees/bt_pre_order.py` · test: `tests/test_bt_pre_order.py`
>
> 📚 Need more detail? See the [in-depth version](bt_pre_order.deep.md).

## Intuition
A "traversal" just means visiting every node once and writing down its value in
some order. Pre-order means: **visit the node first, then its left subtree, then
its right subtree** ("pre" = the node is handled *before* its children). Think of
reading a table of contents top-down: you announce a chapter heading, then dive
into all its sections, before moving on to the next chapter. Pre-order is handy
when you want to copy or serialize a tree, because the root always comes first.

## How it works
We use the given `BinaryNode` (fields: `value`, `left`, `right`). The recipe is a
tiny recursive helper that appends into a shared `out` list.

1. If the current node is `None`, do nothing and return (base case — an empty
   spot adds no values).
2. Append `node.value` to the output. **(visit the node)**
3. Recurse into `node.left`.
4. Recurse into `node.right`.

Trace it on the fixture tree:

```
          20
        /    \
       10     50
      /  \   /  \
     5   15 30  100
```

- Visit 20, go left.
- Visit 10, go left. Visit 5 (leaf), back up. Visit 15 (leaf), back up.
- Back at 20, go right. Visit 50, go left. Visit 30 (leaf). Visit 100 (leaf).

Output order: `[20, 10, 5, 15, 50, 30, 100]` — exactly what the test expects.

## Complexity
- **Time:** O(n) — every node is visited exactly once.
- **Space:** O(h) — the recursion stack holds at most one node per level, where
  `h` is the tree height (O(log n) if balanced, O(n) if it degenerates to a chain).

We touch each node once and the only extra memory is the call stack down one path.

## Common pitfalls
- Forgetting the `None` base case → `AttributeError` when you hit a missing child.
- Mixing up the three orders: pre-order appends the value **before** recursing.
- Appending the *node* instead of `node.value` (tests compare a `list[int]`).
- Creating a fresh list inside the recursion and losing results — append into one
  shared list (or return concatenations).
- Recursing right before left, which silently flips the output.

## Your task
Implement in `src/topics/trees/bt_pre_order.py`, then run:

```bash
uv run pytest -k bt_pre_order
```

Peek at `solutions/bt_pre_order.py` only once you've given it a real attempt.
