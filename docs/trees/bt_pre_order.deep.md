# Binary Tree Pre-order Traversal — In Depth

> In-depth companion · trees · stub: `src/topics/trees/bt_pre_order.py` · test: `tests/test_bt_pre_order.py`
>
> New here? Read the [quick version](bt_pre_order.md) first.

## The mental model

A *traversal* is a rule for visiting every node of a tree exactly once and
writing down its value as you go. The only thing that distinguishes the three
depth-first orders (pre / in / post) is **when** you write down the current
node's value relative to recursing into its children.

Pre-order = **N L R**: handle the **N**ode, then the **L**eft subtree, then the
**R**ight subtree. "Pre" because the node is emitted *before* its descendants.

The tree we use throughout these docs is the fixture
`SAMPLE_TREE_LEVEL_ORDER = [20, 10, 50, 5, 15, 30, 100]`:

```
          20
        /    \
       10     50
      /  \    /  \
     5   15  30  100
```

`pre_order(root)` on this tree returns `[20, 10, 5, 15, 50, 30, 100]`. Notice the
root comes first — that is the signature of pre-order and the reason it is the go-to
order for *copying* or *serializing* a tree.

## Why it works — the invariant

There is no ordering invariant on the *data* (pre-order works on any binary tree,
BST or not). The invariant is on the **algorithm's promise**: a call
`_walk(node)` appends, in order, `node.value` followed by every value in `node`'s
left subtree followed by every value in `node`'s right subtree — and nothing else.

If you trust that promise for the two child calls, the parent call is correct by
construction: emit `node.value` (the node itself), then delegate the left subtree
to a recursive call (which by the promise emits exactly that subtree's values in
pre-order), then the right. This is *structural induction*: the base case (an
empty tree emits nothing) plus the inductive step (a node = value + left block +
right block) covers every finite tree.

## Detailed walkthrough

The reference uses a helper that appends into one shared list:

```python
def pre_order(root):
    out = []
    _walk(root, out)
    return out

def _walk(node, out):
    if node is None:        # base case
        return
    out.append(node.value)  # (1) emit BEFORE recursing
    _walk(node.left, out)   # (2)
    _walk(node.right, out)  # (3)
```

Watch the call stack and the **exact moment** each value is appended. Indentation
shows stack depth; `>>` marks the append.

```
_walk(20)
  >> append 20            out=[20]
  _walk(10)
    >> append 10          out=[20,10]
    _walk(5)
      >> append 5         out=[20,10,5]
      _walk(None) -> ret  (5.left)
      _walk(None) -> ret  (5.right)
    _walk(15)
      >> append 15        out=[20,10,5,15]
      (both children None)
    return (10 done)
  _walk(50)
    >> append 50          out=[20,10,5,15,50]
    _walk(30)
      >> append 30        out=[20,10,5,15,50,30]
    _walk(100)
      >> append 100       out=[20,10,5,15,50,30,100]
    return (50 done)
  return (20 done)
```

Final: `[20, 10, 5, 15, 50, 30, 100]`. The append always happens the instant we
*enter* a node, before we have looked at either child.

## Complexity, derived

- **Time: O(n).** Every node triggers exactly one `_walk` call that does its append
  (plus two calls on `None` children that return immediately). The work per node is
  constant, so total work is proportional to the node count `n`.
- **Space: O(h)**, where `h` is the height. At any instant the call stack holds the
  chain of ancestors from the root down to the node currently executing — that chain
  is at most `h` frames deep. We are not storing a frame per node, only per *level*.
  - Balanced tree: `h ≈ log₂ n`, so space ≈ O(log n).
  - Degenerate "chain" tree (each node has one child): `h = n`, so space = O(n).

The output list is O(n) too, but that is required output, not auxiliary working
space.

## Edge cases in detail

- **Empty tree (`None`).** `test_empty` calls `pre_order(None)`. The first thing
  `_walk` does is the `None` check, so it returns immediately and `out` stays `[]`.
  This base case is what makes the recursion terminate at all.
- **Single node.** `test_single_node` builds `[42]`. `_walk(42)` appends 42, then
  recurses into two `None` children that do nothing → `[42]`.
- **Right-leaning chain** (like `[1, None, 2, None, 3]` used in the BFS tests): the
  left recursions are all immediate returns, so the output is just the chain
  top-to-bottom: `[1, 2, 3]`. This is also the worst case for stack depth.

## Variations & trade-offs

- **Iterative with an explicit stack.** Push the root; pop a node, emit it, then
  push **right first, then left** (so left is popped first — a stack is LIFO):

  ```python
  stack = [root]
  while stack:
      node = stack.pop()
      if node is None:
          continue
      out.append(node.value)
      stack.append(node.right)  # pushed first => popped last
      stack.append(node.left)
  ```

  Same O(n) time and O(h) space, but you control the stack explicitly (handy in
  languages without deep recursion, or to avoid Python's recursion-limit on a
  degenerate tree).
- **Morris traversal** rewires `right` pointers temporarily to walk the tree in
  O(1) extra space (no stack at all). Clever but mutates the tree mid-walk; rarely
  worth it in practice — mentioned so you know it exists.
- **When pre-order is the right tool:** copying/cloning a tree, serializing it to a
  list you can rebuild from (root first means you always have the parent before its
  children), and prefix-expression output.

## Connections

- [in-order](bt_in_order.deep.md) and [post-order](bt_post_order.deep.md): the same
  recursion with the append moved to a different line.
- [BFS / level-order](bt_bfs.deep.md): the *breadth*-first alternative — goes wide
  with a queue instead of deep with a stack.
- Iterative DFS leans on a stack — see [`../linear/stack.md`](../linear/stack.md).
- The same depth-first idea generalizes to graphs (where you must track *visited*
  nodes): [`../graphs/dfs_graph_list.md`](../graphs/dfs_graph_list.md).

## Self-check

1. Without re-reading, write the order of appends for the fixture tree. Where does
   `20` land and why?
2. What single line do you move (and to where) to turn pre-order into post-order?
3. Why is the recursion-stack space O(h) and not O(n) in general?
4. In the iterative version, why do we push the **right** child before the left?
5. For a serialized copy of a tree, why is pre-order more convenient than in-order?
6. What goes wrong if you delete the `if node is None: return` line?

## Deep dive: common bugs

- **Missing the `None` base case.** Without it, `_walk(node.left)` eventually
  receives `None` and `node.value` raises `AttributeError: 'NoneType' object has no
  attribute 'value'`. The base case is non-negotiable.
- **Appending at the wrong moment.** Putting `out.append` *after* the left recursion
  gives in-order; after both gives post-order. The position of that one line *is*
  the algorithm.
- **Recursing right before left.** Silently produces `[20,50,...]` — it mirrors
  every level. Tests compare an exact list, so this fails loudly, but the bug is
  easy to introduce.
- **Appending the node object** instead of `node.value`. Tests expect `list[int]`;
  a list of `BinaryNode` will not compare equal.
- **A fresh list per call.** If `_walk` creates its own list and returns it without
  the parent collecting it, results vanish. Use one shared `out` (or return and
  concatenate, consistently).
