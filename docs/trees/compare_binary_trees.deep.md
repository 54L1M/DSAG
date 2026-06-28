# Compare Two Binary Trees — In Depth

> In-depth companion · trees · stub: `src/topics/trees/compare_binary_trees.py` · test: `tests/test_compare_binary_trees.py`
>
> New here? Read the [quick version](compare_binary_trees.md) first.

## The mental model

Two binary trees are "the same" only if they agree on **both** things at once:

- **Structure** — wherever one tree has a node, the other has a node; wherever one
  has an empty spot, so does the other.
- **Values** — the nodes that line up hold equal values.

The technique is **lockstep recursion**: walk *both* trees together, taking the
same step on `a` and on `b` at the same time, comparing the pair `(a, b)` at each
position. The instant any pair disagrees, the whole answer is `False`. Think of
laying two transparency sheets on top of each other: every dot must coincide.

`compare` returns a `bool`. The fixture trees here are arbitrary (not necessarily
BSTs); structure-plus-value equality has nothing to do with ordering.

## Why it works — the invariant

The function's promise: `compare(a, b)` returns `True` **iff** the subtree rooted
at `a` is identical (same shape, same values) to the subtree rooted at `b`.

Two subtrees are identical exactly when their roots match *and* their left
subtrees are identical *and* their right subtrees are identical. That recursive
definition is the algorithm. The four cases below are a total decision over the
pair `(a, b)` — every possible pair lands in exactly one case, which is why the
recursion is both correct and guaranteed to terminate (each step strictly descends
toward leaves/`None`).

## The four-case lockstep

At each paired position `(a, b)`, in this **exact order**:

1. **Both `None`** → these positions are equal (an empty spot matches an empty
   spot) → return `True`.
2. **Exactly one `None`** → structures differ (one tree has a node, the other a
   gap) → return `False`.
3. **Values differ** (`a.value != b.value`) → return `False`.
4. **Otherwise** → roots agree; recurse on **both** sides and require both:
   `compare(a.left, b.left) and compare(a.right, b.right)`.

```python
def compare(a, b):
    if a is None and b is None:   # case 1: both empty
        return True
    if a is None or b is None:    # case 2: exactly one empty
        return False
    if a.value != b.value:        # case 3: value mismatch
        return False
    return compare(a.left, b.left) and compare(a.right, b.right)  # case 4
```

**Order matters.** Case 1 must precede case 2: by the time we reach `a is None or b
is None`, we already know they are *not both* `None`, so that test cleanly means
"exactly one is `None`." And both `None`-checks must precede case 3, because
`a.value` would raise `AttributeError` if `a` were `None`. The structure check
*guards* the value check.

### Why both structure and value matter

Drop either half and you get false positives:

- **Values only, no structure check:** trees `[1, 2, 3, 4]` and `[1, 2, 3]`
  (`test_different_structure`) could look "equal" if you only compared the values you
  happen to land on — but one tree has a 4th node where the other has a gap. Case 2
  catches it: at that position one side is a node and the other is `None`.
- **Structure only, no value check:** two trees with the same shape but a `30` vs a
  `31` would wrongly match. Case 3 catches it.

## Detailed walkthrough

Compare two copies of the fixture tree:

```
          20                 20
        /    \             /    \
       10     50          10     50
      /  \    /  \        /  \    /  \
     5   15  30  100     5   15  30  100
```

```
compare(20,20)  values equal -> recurse both
  compare(10,10) equal -> recurse both
    compare(5,5)   equal -> recurse both
      compare(None,None) -> True   (5.left vs 5.left)
      compare(None,None) -> True   (5.right vs 5.right)
      -> True
    compare(15,15) -> True
    -> True
  compare(50,50) -> ... -> True
  -> True
-> True
```

Now suppose the second tree had `31` where `30` is. The walk proceeds identically
until `compare(30, 31)`: case 3 fires (`30 != 31`) and returns `False`. That
`False` propagates up through the `and` chain and the whole call returns `False` —
see short-circuiting next.

## Short-circuit evaluation

`compare(a.left, b.left) and compare(a.right, b.right)` uses Python's `and`, which
**short-circuits**: if the left operand is `False`, the right operand is **never
evaluated**. So the moment the left subtrees are found unequal, we skip comparing
the right subtrees entirely and bubble `False` upward. This both saves work on
mismatched inputs and is a clean way to express "all of these must hold." (The
function does *not* early-exit across siblings beyond this — it is the `and` that
prunes.)

## Complexity, derived

- **Time: O(n)** in the worst case, where `n` is the size of the smaller tree. Equal
  (or nearly equal) trees force a visit to every paired position. A mismatch makes it
  faster — short-circuiting can stop early — so O(n) is the upper bound.
- **Space: O(h)** for the recursion stack, `h` = height. Balanced → O(log n);
  degenerate chain → O(n). We only hold one root-to-node path of pending calls.

## Edge cases in detail

- **Both empty.** `test_both_empty`: `compare(None, None)` → case 1 → `True`.
- **One empty.** `test_one_empty`: `compare(tree, None)` and `compare(None, tree)`
  → case 2 → `False` (both directions).
- **Equal trees.** `test_equal_trees`: identical `[1,2,3,4,5]` trees → every pair
  matches → `True`.
- **Different values, same shape.** `test_different_values`: `[1,2,3]` vs `[1,2,4]`
  → case 3 at the `3`/`4` pair → `False`.
- **Different structure.** `test_different_structure`: `[1,2,3,4]` vs `[1,2,3]` →
  case 2 where one tree has the extra node → `False`.

## Variations & trade-offs

- **Iterative lockstep** with an explicit stack/queue of pairs:

  ```python
  stack = [(a, b)]
  while stack:
      x, y = stack.pop()
      if x is None and y is None:
          continue
      if x is None or y is None or x.value != y.value:
          return False
      stack.append((x.left, y.left))
      stack.append((x.right, y.right))
  return True
  ```

  Same O(n)/O(h) profile; avoids Python's recursion limit on deep trees.
- **Serialize-and-compare.** Turn each tree into a string/list (e.g. a pre-order
  with explicit `None` markers) and compare the sequences. Conceptually simple but
  allocates O(n) extra and can't short-circuit as early.
- **Subtree / mirror checks** are close cousins: "is `b` a subtree of `a`?" runs
  `compare` at every node of `a`; a symmetry check compares
  `compare(a.left, b.right) and compare(a.right, b.left)`.

## Connections

- Built on the same depth-first recursion as the traversals:
  [pre-order](bt_pre_order.deep.md), [in-order](bt_in_order.deep.md),
  [post-order](bt_post_order.deep.md).
- The iterative version uses a stack — [`../linear/stack.md`](../linear/stack.md);
  a pair-queue variant would use [`../linear/queue.md`](../linear/queue.md).
- Comparing/visiting structures generalizes to graphs:
  [`../graphs/dfs_graph_list.md`](../graphs/dfs_graph_list.md).

## Self-check

1. Why must the "both `None`" check come before the "exactly one `None`" check?
2. Give a concrete pair of trees that pass a values-only check but should be `False`.
3. What does short-circuit `and` save you, and on which inputs?
4. Why does reading `a.value` before the `None` checks risk an `AttributeError`?
5. What is the time complexity for two *equal* trees vs two trees that differ at the
   root?
6. How would you adapt `compare` to test whether two trees are mirror images?

## Deep dive: common bugs

- **Comparing values but not structure** (or vice versa). Both must hold; the four
  cases together enforce it. Skipping the `None` cases lets different-shaped trees
  pass.
- **Wrong `None`-case order.** Putting the one-`None` test first means two empty
  trees report `False`. Both-`None` first, then one-`None`.
- **Touching `.value` before the guards** → `AttributeError` on a `None` node.
- **Using `or` instead of `and`** in case 4, or recursing only on the left subtree —
  both wrongly accept trees that differ on the right.
- **Returning a truthy node** instead of a real `bool` (the tests use `is True` /
  `is False`, so a node object would fail even if "truthy").
