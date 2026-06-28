# Doubly Linked List — In Depth

> In-depth companion · linked_lists · stub: `src/topics/linked_lists/doubly_linked_list.py` · test: `tests/test_doubly_linked_list.py`
>
> New here? Read the [quick version](doubly_linked_list.md) first.

## The mental model

A doubly linked list is a [singly linked list](singly_linked_list.deep.md) with
one extra arrow per node. Each node now holds three things: a `value`, a `next`
pointer (the node after it), and a `prev` pointer (the node before it).

```
None <- [1] <-> [2] <-> [3] -> None
        ^head            ^tail
```

Reading the arrows carefully: `1.prev is None`, `1.next is 2`, `2.prev is 1`,
`2.next is 3`, `3.next is None`. The backward arrows are not decoration — they
let you (a) walk the list in reverse, and (b) **remove a node in O(1) when you
only hold that node**, because `node.prev` tells you its predecessor for free. A
singly list can't do that; it must scan from the head to find the predecessor.

The node:

```python
class _Node:
    __slots__ = ("value", "prev", "next")
    def __init__(self, value):
        self.value = value
        self.prev = None
        self.next = None
```

The list object holds the same three fields as before: `head`, `tail`, `length`.

## Why it works — the invariant

1. **`length` equals the node count** reachable from `head` via `next` (and,
   equivalently, from `tail` via `prev`).
2. **Both ends are capped**: `head.prev is None` and `tail.next is None`.
3. **The mirror law**: for every node, `node.next.prev is node` and
   `node.prev.next is node` (whenever those neighbors exist). The forward and
   backward chains must agree perfectly — this is the invariant that makes
   doubly-linked code tricky, because *every* splice touches up to four pointers.
4. **Empty ⟺ `head is None` ⟺ `tail is None` ⟺ `length == 0`.**

If you ever break the mirror law — fix `next` but forget the matching `prev` —
the list is corrupt even though a forward walk still "looks" fine. The reverse
walk would reveal the lie.

## Detailed walkthrough

**`prepend(item)` — O(1).** Four pointers in play; do them in a safe order.

```
before:  None <- [1] <-> [2] -> None ; head -> [1]
new:             [9]
step 1: node.next = head            [9] -> [1]
step 2: head.prev = node            [9] <- [1]    (mirror!)
step 3: head = node          head -> [9] <-> [1] <-> [2] -> None
```

If the list was empty, `head` was `None`, so guard step 2 with
`if self.head is not None` and also set `tail = node`.

**`append(item)` — O(1).** The mirror image of `prepend`, working off `tail`.

```
before:  None <- [1] <-> [2] -> None ; tail -> [2]
step 1: node.prev = tail            [2] <- [3]
step 2: tail.next = node            [2] -> [3]
step 3: tail = node          ... <-> [2] <-> [3] -> None
```

Empty case: set `head = node` too. Notice both end-operations are genuinely
O(1) here — no walking, unlike `insert_at`.

**`insert_at(item, index)` — O(n) to walk, O(1) to link.** `index == 0` →
`prepend`; `index == length` → `append`. Otherwise grab the node *currently* at
`index` (call it `cur`), and its `prev`, then weave the new node between them:

```
insert 9 at index 2:
        cur = node_at(2)            ... <-> [2] <-> [3] <-> ...
                                            ^prev   ^cur
        node.prev = prev ; node.next = cur
        prev.next = node ; cur.prev = node
        ... <-> [2] <-> [9] <-> [3] <-> ...
```

Four assignments, all O(1) once you've located `cur`. The walk to find `cur` is
the only O(n) part.

**`get(index)` — O(n), but smarter.** Because we can walk from either end,
`_node_at` walks from `head` when `index <= length // 2` and from `tail`
otherwise. Worst case is still O(n), but the constant halves — a small win the
singly list can't have.

**`remove_at` / `remove` — O(n) to find, O(1) to unlink.** Both funnel into one
helper `_remove_node(node)`:

```python
def _remove_node(self, node):
    if node.prev is not None:
        node.prev.next = node.next     # bridge forward
    else:
        self.head = node.next          # node was the head
    if node.next is not None:
        node.next.prev = node.prev     # bridge backward
    else:
        self.tail = node.prev          # node was the tail
    self.length -= 1
    return node.value
```

This is the payoff of the second pointer: given just the node, we rewire both
neighbors and fix the head/tail ends without ever scanning. `remove_at` walks to
the node first; `remove` scans for a matching value first; the unlink is shared.

```
remove the middle node [2]:
        None <- [1] <-> [2] <-> [3] -> None
        [1].next = [3]   (node.prev.next = node.next)
        [3].prev = [1]   (node.next.prev = node.prev)
        None <- [1] <-> [3] -> None        ([2] now unreachable)
```

## Complexity, derived

| Operation     | Time   | Why |
|---------------|--------|-----|
| `prepend`     | O(1)   | Fixed 3–4 pointer writes. |
| `append`      | O(1)   | Same, off `tail`. |
| `get`         | O(n)   | Still no random access (but ~½ the hops via two-end walk). |
| `insert_at`   | O(n)   | O(n) walk to locate, O(1) to weave 4 pointers. |
| `remove_at`   | O(n)   | O(n) walk, O(1) unlink. |
| `remove`      | O(n)   | Linear scan for the value, O(1) unlink. |
| `length`      | O(1)   | Stored. |

The asymptotics match the singly list — the second pointer doesn't change the
big-O of these methods. What it *does* change: removal given a node handle drops
from O(n) (singly: must find predecessor) to O(1) (doubly: `node.prev` is right
there). That's why LRU caches and `collections.deque` are doubly linked.

## Edge cases in detail

- **Remove head vs. tail vs. middle** (`test_remove_at_all_positions`). The test
  removes index 0 (head), then the new last index (tail), then drains the rest.
  Each path exercises a different branch of `_remove_node`: head removal nulls
  `head`'s side, tail removal nulls `tail`'s side, middle removal bridges both
  neighbors. All three must keep the mirror law intact.

- **Remove the only node.** Both `node.prev` and `node.next` are `None`, so both
  `else` branches fire: `head = None` and `tail = None`. The list collapses to
  empty correctly.

- **Relink after a middle removal** (`test_remove_value_and_relink`). After
  `remove(2)` from `[1,2,3]`, the test appends `4` and re-reads everything. If
  the backward pointers weren't fixed, `append` (which reads `tail` and writes
  `node.prev = tail`) would build a broken chain. The test catches a half-done
  unlink.

- **`index == length` appends; `index > length` raises**
  (`test_out_of_range_raises`) — identical contract to the singly list.

## Variations & trade-offs

- **When a doubly list beats a singly list.** You need backward traversal; or
  you hold node references and want O(1) deletion (caches, intrusive lists); or
  you want genuinely O(1) operations at *both* ends (a deque).

- **Cost of the second pointer.** Extra memory per node (one more reference) and
  more pointer writes per mutation — more places to get the mirror law wrong.
  If you only ever push/pop one end, a singly list (or a stack/queue) is leaner.

- **Sentinel nodes.** Production implementations often use dummy `head`/`tail`
  sentinels so there are no `None` checks at the ends — every real node always
  has neighbors. This trades a little memory for branch-free splice code.

- **`collections.deque`** is the batteries-included doubly linked list; prefer
  it in real code.

## Connections

- Compare directly with the [singly linked list](singly_linked_list.deep.md) —
  same interface, one extra pointer.
- The [LRU cache](../cache/lru.md) is the canonical use: a hash map of keys →
  nodes plus a doubly linked list for recency, so touching an entry is O(1).
- The two-end walk in `_node_at` is a baby version of the bidirectional search
  idea you'll meet in graph algorithms.

## Self-check

1. State the mirror law. Give an example of code that fixes `next` but violates
   it.
2. In `_remove_node`, what do the two `else` branches handle, and when do *both*
   fire at once?
3. Why are `prepend` and `append` both O(1) here, but `insert_at` is O(n)?
4. `get(index)` walks from the nearer end. Does this change the big-O? What does
   it change?
5. After `remove(2)` from `[1,2,3]`, exactly which pointers were rewritten?
6. Why can a doubly list delete a node in O(1) given only the node, while a
   singly list cannot?

## Deep dive: common bugs

- **Breaking the mirror law.** Setting `prev.next = node` but forgetting
  `cur.prev = node` (or vice versa) leaves the forward and backward chains
  disagreeing. A forward walk hides it; a reverse walk or a later `append`
  exposes it. Always update both directions in the same breath.

- **Losing the rest of the list.** As in the singly list, save `node.next` /
  `node.prev` before overwriting them, or you orphan the tail of the list.

- **Forgetting to update `tail` (or `head`).** Append/remove at the ends must
  move the matching end pointer. The `_remove_node` `else` branches exist
  exactly for this; drop one and an end pointer dangles.

- **Forgetting `length`.** Same as everywhere: `+= 1` / `-= 1` on every mutation
  or the bounds checks rot.

- **Off-by-one in the two-end walk.** Walking from the tail uses
  `range(length - 1 - index)` steps. Getting that arithmetic wrong returns the
  neighbor of the node you wanted — a subtle, position-dependent bug.

- **Unguarded end writes.** On an empty list `head`/`tail` are `None`; writing
  `head.prev = node` without the `if self.head is not None` guard throws
  `AttributeError`. Every end operation needs the empty-list guard.
