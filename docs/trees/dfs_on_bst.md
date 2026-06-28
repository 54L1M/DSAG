# DFS Find on a Binary Search Tree

> trees · stub: `src/topics/trees/dfs_on_bst.py` · test: `tests/test_dfs_on_bst.py`
>
> 📚 Need more detail? See the [in-depth version](dfs_on_bst.deep.md).

## Intuition
A **binary search tree (BST)** keeps an invariant at every node: everything in the
**left** subtree is smaller than the node's value, and everything in the **right**
subtree is larger. Searching for a value exploits this — at each node you compare
once and confidently throw away *half* the tree, just like looking up a word in a
dictionary by flipping toward the right region instead of reading every page. The
function returns a `bool`: `True` if the value exists, `False` otherwise.

## How it works
We use the given `BinaryNode` (fields: `value`, `left`, `right`). You can write
this recursively or with a simple loop — both walk a single root-to-leaf path.

1. Start at `root`.
2. While the current node is not `None`:
   - If `value == node.value` → found it, return `True`.
   - If `value < node.value` → it can only be left, so move to `node.left`.
   - Else (`value > node.value`) → move to `node.right`.
3. If you fall off the tree (reach `None`), the value isn't there → `False`.

Trace `find(root, 30)` on the fixture BST:

```
          20
        /    \
       10     50
      /  \   /  \
     5   15 30  100
```

- At 20: 30 > 20 → go **right** (skip the entire 10/5/15 subtree).
- At 50: 30 < 50 → go **left**.
- At 30: equal → return `True`.

Only 3 nodes examined out of 7. `find(root, 11)` would go 20 → left 10 → right 15
→ left `None` → `False`.

## Complexity
- **Time:** O(h) — one comparison per level, where `h` is the height
  (O(log n) for a balanced BST, O(n) for a degenerate chain).
- **Space:** O(1) for the iterative loop, or O(h) recursion stack if you recurse.

Because each step discards one whole subtree, you never scan all `n` nodes.

## Common pitfalls
- Treating it like a plain tree search that scans **both** children — that throws
  away the BST advantage and becomes O(n). Pick one side using the comparison.
- Getting the comparison backwards (going right when `value < node.value`), which
  misses present values.
- Forgetting the `None` base case → crash or infinite loop.
- Assuming the input is a BST when it isn't — this only works on a valid BST.
- Returning a node (or `None`) instead of a real `bool`.

## Your task
Implement in `src/topics/trees/dfs_on_bst.py`, then run:

```bash
uv run pytest -k dfs_on_bst
```

Peek at `solutions/dfs_on_bst.py` only once you've given it a real attempt.
