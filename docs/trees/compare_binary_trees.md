# Compare Two Binary Trees

> trees · stub: `src/topics/trees/compare_binary_trees.py` · test: `tests/test_compare_binary_trees.py`
>
> 📚 Need more detail? See the [in-depth version](compare_binary_trees.deep.md).

## Intuition
Two binary trees are "the same" only if they have the **identical shape** *and*
the **identical values** at every position. We check this by walking both trees in
**lockstep** — the same step on tree `a` and tree `b` at the same time — and the
moment anything disagrees, the answer is `False`. Think of overlaying two
transparency sheets: if every dot lines up, they match; one stray or missing dot
and they don't. The function returns a `bool`.

## How it works
We use the given `BinaryNode` (fields: `value`, `left`, `right`). At each pair of
nodes `(a, b)` there are four cases:

1. **Both `None`** → these positions match (nothing here on either side) → `True`.
2. **Exactly one `None`** → shapes differ (one tree has a node, the other a gap) →
   `False`.
3. **Values differ** (`a.value != b.value`) → `False`.
4. **Otherwise** recurse on **both** sides and require both to hold:
   `compare(a.left, b.left) and compare(a.right, b.right)`.

The `and` short-circuits: if the left subtrees already disagree, we never bother
with the right.

Example using two copies of the fixture tree:

```
          20                 20
        /    \             /    \
       10     50          10     50
      /  \   /  \        /  \   /  \
     5   15 30  100     5   15 30  100
```

Every paired node matches in value and structure, so each recursive call returns
`True` and the overall result is `True`. If, say, the second tree had `31` instead
of `30`, case 3 would fire at that pair and the whole comparison collapses to
`False`.

## Complexity
- **Time:** O(n) — in the worst case (equal trees) we visit every pair of nodes
  once, where `n` is the size of a tree.
- **Space:** O(h) — recursion stack depth equals the tree height `h`
  (O(log n) balanced, O(n) for a degenerate chain).

We compare each position once; the call stack only holds one root-to-node path.

## Common pitfalls
- Checking values but **not** structure (or vice versa) — you must compare both.
- Getting the `None` cases wrong: both-`None` is `True`, one-`None` is `False`.
  Order matters — test both-`None` *before* the one-`None` check.
- Reading `a.value` before confirming `a` is not `None` → `AttributeError`.
- Recursing only on the left subtree and forgetting the right (or `or` instead of
  `and`).
- Returning a truthy node object instead of a real `bool`.

## Your task
Implement in `src/topics/trees/compare_binary_trees.py`, then run:

```bash
uv run pytest -k compare_binary_trees
```

Peek at `solutions/compare_binary_trees.py` only once you've given it a real attempt.
