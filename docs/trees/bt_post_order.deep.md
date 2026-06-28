# Binary Tree Post-order Traversal — In Depth

> In-depth companion · trees · stub: `src/topics/trees/bt_post_order.py` · test: `tests/test_bt_post_order.py`
>
> New here? Read the [quick version](bt_post_order.md) first.

## The mental model

The third member of the depth-first family. Same recursion, append moved again.
Post-order = **L R N**: recurse into the **L**eft subtree, then the **R**ight
subtree, then emit the **N**ode. "Post" because the node is emitted *after* both of
its children are completely done.

The mental hook: you cannot finish a parent until its children are finished.
Deleting a directory tree, computing a folder's total size, freeing memory, or
evaluating an arithmetic expression bottom-up — all are "children first, then
combine into the parent" jobs, which is exactly post-order.

Fixture tree (`SAMPLE_TREE_LEVEL_ORDER = [20, 10, 50, 5, 15, 30, 100]`):

```
          20
        /    \
       10     50
      /  \    /  \
     5   15  30  100
```

`post_order(root)` returns `[5, 15, 10, 30, 100, 50, 20]`. The root is always the
**last** element — that is the fingerprint of post-order.

## Why it works — the invariant

Like pre-order, post-order works on any binary tree; there is no data invariant.
The algorithm's promise is: `_walk(node)` appends every value in the left subtree
(in post-order), then every value in the right subtree (in post-order), then
`node.value` last.

By structural induction: trust the two child calls to emit their subtrees in
post-order, then append the node afterward. Because a node is emitted strictly
after *everything beneath it*, the output has a useful property — **every node
appears after all of its descendants**. That is precisely the safe order to
destroy/free a structure (you never free a parent while a child still points into
it) or to fold values upward (every child's contribution is ready before the
parent combines them).

## Detailed walkthrough

```python
def _walk(node, out):
    if node is None:
        return
    _walk(node.left, out)   # (1)
    _walk(node.right, out)  # (2)
    out.append(node.value)  # (3) emit AFTER both children
```

Call stack with exact append moments (`>>`):

```
_walk(20)
  _walk(10)
    _walk(5)
      _walk(None) -> ret     (5.left)
      _walk(None) -> ret     (5.right)
      >> append 5    out=[5]
    _walk(15)
      >> append 15   out=[5,15]
    >> append 10     out=[5,15,10]    # 10 only AFTER 5 and 15
  _walk(50)
    _walk(30)
      >> append 30   out=[5,15,10,30]
    _walk(100)
      >> append 100  out=[5,15,10,30,100]
    >> append 50     out=[5,15,10,30,100,50]   # 50 after 30 and 100
  >> append 20       out=[5,15,10,30,100,50,20] # root LAST
```

Final: `[5, 15, 10, 30, 100, 50, 20]`. Each parent's append is the *last thing*
its `_walk` does, after both children have fully returned.

## Complexity, derived

- **Time: O(n).** One `_walk` per node, constant work per node.
- **Space: O(h)** for the recursion stack (the ancestor chain).
  - Balanced: O(log n). Degenerate chain: O(n).

Identical bounds to pre- and in-order: the *shape* of the recursion is the same;
only the emission point differs, and that costs nothing.

## Edge cases in detail

- **Empty tree.** `test_empty`: `post_order(None)` returns `[]` via the base case.
- **Single node.** `test_single_node` builds `[42]`: both child recursions return,
  then append 42 → `[42]`.
- **Right-leaning chain** `[1, None, 2, None, 3]`: left recursions are empty; you go
  all the way down before emitting anything, then unwind appending bottom-up →
  `[3, 2, 1]`. Note this is the *reverse* of the value order here — a nice reminder
  that post-order emits deepest-first.

## Variations & trade-offs

- **Iterative — the "two stacks" trick.** Do a *modified pre-order* that visits
  N R L, pushing each emitted value onto a second stack; the second stack popped is
  post-order:

  ```python
  s1, s2 = [root], []
  while s1:
      node = s1.pop()
      if node is None:
          continue
      s2.append(node.value)
      s1.append(node.left)   # left pushed first
      s1.append(node.right)  # so right is processed first -> N R L
  out = s2[::-1]             # reverse of N R L == L R N
  ```

  O(n) time, O(n) space. A single-stack iterative post-order also exists but needs a
  "last visited" pointer to know when to emit a node — fiddlier.
- **Morris post-order** is possible but the trickiest of the three; mention only.
- **When post-order is the right tool:** freeing/deleting a tree, computing
  aggregates that depend on children (subtree size, height, sum), and converting an
  expression tree to postfix (Reverse Polish) notation.

## Connections

- [pre-order](bt_pre_order.deep.md) (N L R) and [in-order](bt_in_order.deep.md)
  (L N R): the family — same recursion, append relocated.
- [BFS / level-order](bt_bfs.deep.md): the breadth-first alternative.
- Iterative versions use an explicit stack — see
  [`../linear/stack.md`](../linear/stack.md).
- Depth-first on graphs (with a visited set): [`../graphs/dfs_graph_list.md`](../graphs/dfs_graph_list.md).

## Self-check

1. Why must the root be the last element of any post-order output?
2. For the fixture, why is 10 emitted only after 5 and 15?
3. Which line moves, and where, to convert this into pre-order?
4. What real-world operation maps naturally onto post-order, and why?
5. On the chain `1 -> 2 -> 3` (right children), what is the post-order, and why is it
   "reversed"?
6. What is the stack depth in the worst case?

## Deep dive: common bugs

- **Missing the `None` base case** → `AttributeError` on a missing child.
- **Appending too early.** Append before the right recursion → a hybrid order;
  append before both → pre-order. The node's append must be the final statement.
- **Expecting the root first.** In post-order the root is **last** — a frequent
  off-by-intuition error when eyeballing output.
- **Swapping left/right recursion** reorders siblings and fails the exact-list test.
- **Returning node objects** rather than `node.value`.
