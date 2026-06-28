# DFS Find on a Binary Search Tree — In Depth

> In-depth companion · trees · stub: `src/topics/trees/dfs_on_bst.py` · test: `tests/test_dfs_on_bst.py`
>
> New here? Read the [quick version](dfs_on_bst.md) first.

## The mental model

A **binary search tree (BST)** is an *ordered* tree. At every node the invariant
holds: everything in the **left** subtree is smaller than the node, everything in
the **right** subtree is larger (`left < node < right`).

Searching exploits that ordering the way you use a dictionary: you don't read every
page, you compare against where you are and jump toward the right region. At each
node, one comparison tells you which *single* subtree could possibly contain your
value — and you throw the other one away. The function `find` returns a `bool`:
`True` if the value is present, `False` otherwise.

Fixture BST (`build_bst([20, 10, 50, 5, 15, 30, 100])`):

```
          20
        /    \
       10     50
      /  \    /  \
     5   15  30  100
```

## Why it works — the invariant

Because `left < node < right` holds *recursively at every node*, a single
comparison is decisive:

- If `value == node.value`, you found it.
- If `value < node.value`, then by the invariant the value, if it exists at all,
  must be in the **left** subtree — every value in the right subtree is `>
  node.value > value`, so the right side cannot contain it. Go left.
- If `value > node.value`, symmetric: it can only be on the **right**. Go right.

This is the heart of it: each step **eliminates an entire subtree** with one
comparison, with no possibility of error, *provided the tree is a valid BST*. That
qualifier is essential — on a non-BST this pruning is unsound and you would miss
present values.

## Detailed walkthrough

The reference is **iterative** (a loop, O(1) extra space):

```python
def find(root, value):
    node = root
    while node is not None:
        if value == node.value:
            return True
        node = node.left if value < node.value else node.right
    return False
```

Trace `find(root, 30)`:

```
node=20   30 > 20  -> go RIGHT   (discard 10/5/15 entirely)
node=50   30 < 50  -> go LEFT
node=30   30 == 30 -> return True
```

Three nodes examined out of seven; the whole `10`-subtree was skipped after one
comparison.

Trace a miss, `find(root, 11)`:

```
node=20   11 < 20  -> go LEFT
node=10   11 > 10  -> go RIGHT
node=15   11 < 15  -> go LEFT
node=None              loop ends -> return False
```

Falling off the tree (reaching `None`) is the proof of absence: we followed the
only path the value could have lived on and it wasn't there.

## Contrast with scanning every node

A naive search that ignores the BST ordering recurses into **both** children
looking for the value — that visits all `n` nodes, O(n), and works on any tree. The
BST `find` instead follows **one** root-to-leaf path, touching at most `h+1` nodes
where `h` is the height. The savings come entirely from the invariant letting you
discard a subtree unseen. Use the ordering, or you have thrown away the only reason
to use a BST.

## Complexity, derived

The work is one comparison per level along a single downward path, so the cost is
the **path length = the height `h`**.

- **Balanced BST: O(log n).** Each step halves the candidate set; after `k` steps
  you've narrowed `n` nodes to `n / 2ᵏ`. You hit a single node (or `None`) when
  `2ᵏ ≈ n`, i.e. `k ≈ log₂ n`. For `n = 1,000,000`, that's ~20 comparisons.
- **Degenerate (skewed) BST: O(n).** If the tree is a chain, `h = n - 1` and you may
  walk the whole thing. **This is exactly what happens with sorted insertion
  order.** Inserting `[1, 2, 3, 4, 5]` into `build_bst` makes every new value larger
  than all before it, so each goes right:

  ```
  1
   \
    2
     \
      3
       \
        4
         \
          5
  ```

  Now `find` is no better than scanning a linked list — O(n). The BST's speed
  advantage depends on *balance*, which depends on insertion order (or on a
  self-balancing variant like an AVL / red-black tree).

- **Space: O(1)** for the iterative reference (just a `node` pointer). A recursive
  version would use **O(h)** stack space instead.

## Edge cases in detail

- **Empty tree.** `test_empty_tree`: `find(None, 5)` — the `while node is not None`
  guard is false immediately, so we return `False` without dereferencing anything.
- **Present values.** `test_finds_present_values` checks all of
  `20, 10, 50, 5, 15, 30, 100` return `True` — each is reachable by following the
  comparisons down its path.
- **Missing values.** `test_missing_values` checks `0, 11, 99, 1000` return `False`.
  Each walk ends by stepping to a `None` child (e.g. `0` goes left from 20, left from
  10, left from 5 into `None`).
- **Single node / value at the root.** `find(root, 20)` returns `True` on the first
  comparison — no descent needed.

## Variations & trade-offs

- **Recursive `find`** — same logic, expressed by recursion:

  ```python
  def find(root, value):
      if root is None:
          return False
      if value == root.value:
          return True
      if value < root.value:
          return find(root.left, value)
      return find(root.right, value)
  ```

  Identical O(h) time, but O(h) **stack** space and a risk of hitting Python's
  recursion limit on a deeply skewed tree. The iterative loop is preferable here.
- **Returning the node** instead of a bool (handy if callers need the payload) — a
  common real-world tweak; this exercise wants a `bool`.
- **Insertion / deletion** follow the same descend-by-comparison path to find where a
  value belongs.
- **Self-balancing BSTs** (AVL, red-black) keep `h ≈ log n` regardless of insertion
  order, restoring guaranteed O(log n). Plain BSTs do not.

## Connections

- The BST invariant `left < node < right` is the same one that makes
  [in-order traversal](bt_in_order.deep.md) come out **sorted** — searching and
  sorted-reading are two uses of one property.
- This is depth-first, like the [traversals](bt_pre_order.deep.md), but it follows a
  *single* path instead of visiting everything.
- The same halving-by-comparison idea on a sorted **array** is
  [`../search/binary_search.md`](../search/binary_search.md) — a BST is essentially
  binary search made into a pointer structure.
- DFS on general graphs (must track visited nodes, may branch):
  [`../graphs/dfs_graph_list.md`](../graphs/dfs_graph_list.md). Iterative DFS uses a
  stack: [`../linear/stack.md`](../linear/stack.md).

## Self-check

1. State the BST invariant and explain why one comparison lets you discard a whole
   subtree.
2. Why is `find` O(log n) on a balanced tree but O(n) on a skewed one?
3. What insertion order produces the O(n) worst case, and what shape does the tree
   take?
4. How does this differ from a naive search that recurses into both children?
5. What is the space cost of the iterative version vs. the recursive version?
6. Why is using `find` on a tree that is *not* a valid BST a bug?

## Deep dive: common bugs

- **Recursing into both subtrees** ("just search everywhere"). Correct answers, but
  O(n) — you've discarded the entire reason to use a BST. Pick **one** side from the
  comparison.
- **Backwards comparison** — going right when `value < node.value` (or vice versa).
  You walk away from the value and report `False` for things that are present; the
  `test_finds_present_values` cases expose it.
- **Missing the `None` / loop-exit case.** Without `while node is not None` (or the
  recursive `if root is None`), you dereference `None` → `AttributeError`, or loop
  forever.
- **Assuming a BST when the input isn't one.** The pruning is only sound under
  `left < node < right`; on an arbitrary tree it silently misses values.
- **Returning a node or `None`** instead of a real `bool` — the tests use
  `is True` / `is False`.
