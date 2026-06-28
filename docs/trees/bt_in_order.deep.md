# Binary Tree In-order Traversal — In Depth

> In-depth companion · trees · stub: `src/topics/trees/bt_in_order.py` · test: `tests/test_bt_in_order.py`
>
> New here? Read the [quick version](bt_in_order.md) first.

## The mental model

Same recursion as the other depth-first traversals — only the moment of emission
changes. In-order = **L N R**: recurse into the **L**eft subtree, then emit the
**N**ode, then recurse into the **R**ight subtree. "In" because the node is emitted
*in between* its two subtrees.

The fixture tree (`SAMPLE_TREE_LEVEL_ORDER = [20, 10, 50, 5, 15, 30, 100]`) is a
**binary search tree (BST)**:

```
          20
        /    \
       10     50
      /  \    /  \
     5   15  30  100
```

`in_order(root)` returns `[5, 10, 15, 20, 30, 50, 100]` — **sorted ascending**.
That is not a coincidence; it is the headline property of in-order on a BST, and
the whole point of `test_sample_tree_is_sorted`.

## Why it works — the invariant

A **BST invariant** holds at *every* node: all values in its left subtree are
**strictly less** than the node's value, and all values in its right subtree are
**strictly greater** (`left < node < right`).

Claim: in-order traversal of a BST emits values in increasing order. Proof by
structural induction. Assume each child call emits its subtree's values sorted
(the inductive hypothesis). For a node `N`:

1. We first emit the entire left subtree — by hypothesis, sorted, and **every one
   of those values is `< N.value`** (BST invariant).
2. We emit `N.value` — and it is greater than everything just emitted.
3. We emit the entire right subtree — sorted, and **every value is `> N.value`**.

So the concatenation `[left block] + [N] + [right block]` is itself sorted: each
block is sorted internally, and the blocks are in the right relative order because
`left < N < right`. The base case (empty subtree) is trivially sorted. Therefore
the whole traversal is sorted. The magic is that the *structure of the tree
already encodes the sort order* — in-order just reads it out.

Walk the fixture: at root 20, the left block must be everything `< 20`
(`5,10,15`) and the right block everything `> 20` (`30,50,100`), with 20 wedged
between. Recurse and the same logic produces each block sorted.

## Detailed walkthrough

```python
def _walk(node, out):
    if node is None:
        return
    _walk(node.left, out)   # (1) whole left subtree first
    out.append(node.value)  # (2) emit BETWEEN the subtrees
    _walk(node.right, out)  # (3)
```

Call stack with the exact append moments (`>>`):

```
_walk(20)
  _walk(10)
    _walk(5)
      _walk(None) -> ret        (5.left)
      >> append 5     out=[5]
      _walk(None) -> ret        (5.right)
    >> append 10      out=[5,10]
    _walk(15)
      >> append 15    out=[5,10,15]
    return (10 done)
  >> append 20        out=[5,10,15,20]
  _walk(50)
    _walk(30)
      >> append 30    out=[5,10,15,20,30]
    >> append 50      out=[5,10,15,20,30,50]
    _walk(100)
      >> append 100   out=[...,100]
    return (50 done)
  return (20 done)
```

Final: `[5, 10, 15, 20, 30, 50, 100]`. Crucially, a node is appended only **after**
its entire left subtree has finished and **before** its right subtree begins — that
sandwiching is what interleaves the values into sorted order.

## Complexity, derived

- **Time: O(n).** One `_walk` per node, constant work each (the append). The
  ordering property costs nothing extra — it falls out of the recursion shape.
- **Space: O(h)** for the call stack (ancestor chain only).
  - Balanced: `h ≈ log₂ n` → O(log n).
  - Degenerate chain: `h = n` → O(n). For example, inserting values in already-sorted
    order builds a right-leaning chain, and in-order then recurses `n` deep.

## Edge cases in detail

- **Empty tree.** `test_empty`: `in_order(None)` → base case returns immediately →
  `[]`.
- **Single node.** `test_single_node` builds `[42]`: left recursion returns, append
  42, right recursion returns → `[42]`.
- **Sorted only for a *valid* BST.** In-order of an arbitrary binary tree still
  visits every node L-N-R, but the output is only sorted if the BST invariant holds.
  Feed in a non-BST and you get a perfectly valid in-order sequence that is *not*
  sorted — a great sanity check on whether a tree really is a BST.
- **Right-leaning chain** `[1, None, 2, None, 3]`: each left recursion is empty, so
  you emit `1, 2, 3` — still sorted, still O(n) depth.

## Variations & trade-offs

- **Iterative with an explicit stack.** Push left children until you hit `None`,
  pop-and-emit, then move to the popped node's right child:

  ```python
  stack, node = [], root
  while stack or node:
      while node:            # dive left, remembering the path
          stack.append(node)
          node = node.left
      node = stack.pop()
      out.append(node.value) # emit when we come back up
      node = node.right
  ```

  O(n) time, O(h) space — same as recursion, but no recursion-limit risk.
- **Morris in-order** achieves O(1) extra space by temporarily threading
  `right`-most nodes back to their in-order successor. Elegant but mutates pointers
  mid-walk; just know the name.
- **When in-order is the right tool:** anything that wants the BST's *sorted* view —
  printing keys in order, finding the k-th smallest, range queries, validating that
  a tree is a BST (in-order must be strictly increasing).

## Connections

- [pre-order](bt_pre_order.deep.md) (N L R) and [post-order](bt_post_order.deep.md)
  (L R N): same code, the append on a different line.
- [DFS find on a BST](dfs_on_bst.deep.md): the *same* `left < node < right` invariant,
  used to **search** in O(h) instead of reading everything out.
- [BFS / level-order](bt_bfs.deep.md): the breadth-first counterpart.
- Iterative version uses a stack — see [`../linear/stack.md`](../linear/stack.md).
- The depth-first pattern on graphs: [`../graphs/dfs_graph_list.md`](../graphs/dfs_graph_list.md).

## Self-check

1. State the BST invariant and use it to explain *why* in-order comes out sorted.
2. For the fixture, which values form the "left block" of the root, and why must
   they all precede 20?
3. If in-order output is **not** sorted, what does that tell you about the tree?
4. Where does the append line sit relative to the two recursive calls?
5. What is the worst-case stack depth, and what insertion order causes it?
6. How would you check "is this a valid BST?" using in-order?

## Deep dive: common bugs

- **Missing the `None` base case** → `AttributeError` when a recursion lands on a
  missing child.
- **Append in the wrong spot.** Append *before* the left recursion → pre-order;
  append *after* the right recursion → post-order. The sorted property silently
  disappears — the test for sortedness is what catches this.
- **Assuming any tree sorts.** In-order only yields sorted output for a *valid* BST.
  Do not rely on it for arbitrary binary trees.
- **Swapping left/right recursion** reverses the sorted order into descending — also
  caught by the exact-list comparison.
- **Returning node objects** instead of `node.value` — tests expect `list[int]`.
