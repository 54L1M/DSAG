# Singly Linked List — In Depth

> In-depth companion · linked_lists · stub: `src/topics/linked_lists/singly_linked_list.py` · test: `tests/test_singly_linked_list.py`
>
> New here? Read the [quick version](singly_linked_list.md) first.

## The mental model

Forget Python's `list` for a moment. A singly linked list is built from tiny
objects called **nodes**. Each node holds two things: a `value`, and a single
arrow `next` that points at the node after it. The last node's `next` is `None`,
which is how we know we've hit the end.

```
head                                  tail
 |                                     |
 v                                     v
[1|•] -> [2|•] -> [3|•] -> None
```

Each `[v|•]` is one node. The `•` is the `next` pointer. The list object itself
holds three small fields and *nothing else*:

- `head` — the first node (or `None` when empty)
- `tail` — the last node (kept so `append` is cheap)
- `length` — how many nodes there are

The whole game is **pointer surgery**: to add or remove an item you re-aim a
couple of arrows. You never copy or shift the other nodes — they stay exactly
where they are in memory. This is the opposite of an array, where inserting at
the front forces every later element to slide over.

A node is just:

```python
class _Node:
    __slots__ = ("value", "next")   # __slots__ saves memory: no per-node __dict__
    def __init__(self, value):
        self.value = value
        self.next = None
```

## Why it works — the invariant

An *invariant* is a statement that is true before and after every operation. If
your invariants hold, the structure is correct. For this list:

1. **`length` equals the number of reachable nodes** starting from `head`.
2. **The chain is `None`-terminated**: follow `next` from `head` and you reach
   `None` in exactly `length` steps.
3. **`tail.next is None`** — the tail is genuinely the last node.
4. **Empty ⟺ `head is None` ⟺ `tail is None` ⟺ `length == 0`**. These three
   facts move together; if one says "empty" they all must.

Every method below is written so that *if* the invariants held on entry, they
still hold on exit. That is the entire correctness argument. When a bug appears,
it is almost always one of these four quietly broken — `length` drifting out of
sync, or `tail` pointing at a node that is no longer last.

## Detailed walkthrough

**`prepend(item)` — O(1).** New node points at the old head; head moves to it.

```
before:  head -> [1|•] -> [2|•] -> None
new node:        [9|•]
step 1: node.next = head      [9|•] -> [1|•] -> ...
step 2: head = node    head -> [9|•] -> [1|•] -> [2|•] -> None
```

If the list was empty, `tail` was `None`, so we also set `tail = node`.

**`append(item)` — O(1) thanks to the tail pointer.** Hang the new node off the
current tail, then advance the tail.

```
before:  head -> [1|•] -> [2|•] -> None ; tail -> [2]
step 1: tail.next = node      [2|•] -> [3|•] -> None
step 2: tail = node           tail -> [3]
```

Without a `tail` pointer you would have to walk from `head` to the end every
time — that is the O(n) trap. The empty case sets `head = tail = node`.

**`insert_at(item, index)` — O(n).** Walk to the node *before* the target slot,
then splice. `index == 0` delegates to `prepend`; `index == length` delegates to
`append` (this is why inserting at the very end is allowed). Otherwise:

```
insert 9 at index 2:
        prev = node_at(1)                  # walk index-1 steps
        head -> [1|•] -> [2|•] -> [3|•] -> None
                          ^prev
step 1: node.next = prev.next   [9|•] -> [3]
step 2: prev.next = node
        head -> [1|•] -> [2|•] -> [9|•] -> [3|•] -> None
```

Order matters: save `prev.next` into `node.next` **first**, then overwrite
`prev.next`. Do it the other way and you lose the tail of the list.

**`get(index)` — O(n).** There is no random access. Start at `head` and follow
`next` exactly `index` times. The helper `_node_at(index)` does this walk and
raises `IndexError` for `index < 0 or index >= length`.

**`remove_at(index)` — O(n).** Removing the head is special: `head = head.next`,
and if that empties the list, reset `tail = None`. Otherwise walk to `prev`,
unlink the node, and if the unlinked node *was* the tail, set `tail = prev`.

```
remove index 1 (value 2):
        prev = node_at(0)
        head -> [1|•] -> [2|•] -> [3|•] -> None
                 ^prev    ^node
        prev.next = node.next
        head -> [1|•] ----------> [3|•] -> None   (node 2 is now unreachable)
```

The orphaned node is garbage-collected automatically — we don't free memory by
hand in Python.

**`remove(item)` — O(n).** Walk with two pointers, `prev` and `cur`. On the
first node whose `value == item`, unlink it (relink `head` if `prev is None`,
fix `tail` if it was the tail) and return the value. Walk off the end without a
match → return `None`. Note `remove` returns `None` on miss, while `remove_at`
*raises* on a bad index — different contracts for different jobs.

## Complexity, derived

| Operation     | Time   | Why |
|---------------|--------|-----|
| `prepend`     | O(1)   | Re-aim two pointers; no walking. |
| `append`      | O(1)   | `tail` lets us jump straight to the end. |
| `get`         | O(n)   | No index math — must hop node by node. |
| `insert_at`   | O(n)   | O(n) to walk to `index-1`, then O(1) to splice. |
| `remove_at`   | O(n)   | O(n) to walk, O(1) to unlink. |
| `remove`      | O(n)   | Linear scan for the value. |
| `length`      | O(1)   | Stored, not counted. |

**Why is `prepend` O(1) but `get` O(n)?** Both touch pointers, but `prepend`
touches a *fixed* number (two) regardless of list size, while `get(index)` must
take `index` hops — and `index` grows with the list. Constant work vs.
size-dependent work: that is exactly the O(1) vs. O(n) distinction.

**Why does a tail pointer make `append` O(1)?** Appending fundamentally needs to
touch the last node. Finding it from `head` costs n hops. Caching it in `tail`
makes "find the last node" a single field read. The price is that *every*
mutation must keep `tail` honest — which is precisely where bugs hide.

## Edge cases in detail

- **Append after emptying must reuse the tail logic**
  (`test_append_after_emptying_uses_tail`). Add one item, remove it, append
  again. When `remove_at(0)` empties the list it must reset `tail = None`. If it
  forgets, `tail` still points at the dead node; the next `append` does
  `tail.next = node` and the new node is attached to a node that `head` can't
  reach — `get(0)` then returns the wrong thing. The test pins this exact bug.

- **Removing the only node.** `head` becomes `None`; you must also null `tail`.
  Both ends collapse together.

- **Removing the tail (not the head).** After `prev.next = node.next`, you must
  notice `node is self.tail` and set `tail = prev`. Otherwise `tail` dangles.

- **`index == length` on insert appends; `index > length` raises**
  (`test_out_of_range_raises`). The boundary is generous on insert (you may
  insert *at* the end) but strict beyond it.

- **`get`/`remove_at` use `index >= length`** as the out-of-range test, because
  the last valid index is `length - 1`. Mixing up `>` and `>=` here is the
  classic off-by-one.

## Variations & trade-offs

- **Array vs. linked list.** An array stores elements contiguously, so `get(i)`
  is O(1) pointer arithmetic and the CPU cache loves the sequential layout. But
  inserting at the front shifts everything (O(n)). A linked list flips this:
  O(1) splice anywhere you already hold a pointer, but O(n) random access and
  poor cache behavior (nodes scattered across memory, each hop a possible cache
  miss). Choose by your access pattern.

- **No tail pointer** → simpler code, but `append` degrades to O(n). Usually not
  worth it.

- **Singly vs. doubly.** A singly list can't walk backward and can't remove a
  node in O(1) when you only hold *that* node (you need its predecessor). When
  you need either, reach for the [doubly linked list](doubly_linked_list.deep.md).

- **`collections.deque`** is a production-grade doubly-linked structure with
  O(1) both ends — in real code you'd use that, not a hand-rolled list.

## Connections

- The [Stack](../linear/stack.deep.md) is *just* a singly linked list that only
  ever touches the head (`prepend`/remove-head renamed `push`/`pop`).
- The [Queue](../linear/queue.deep.md) is a singly linked list using `head` as
  the front and `tail` as the back — `append` + remove-head.
- The two-pointer `prev`/`cur` walk in `remove` reappears everywhere: cycle
  detection, list reversal, merging sorted lists.

## Self-check

1. Why must `insert_at` save `prev.next` into the new node *before* overwriting
   `prev.next`?
2. The list has 3 nodes. You `remove_at(2)` (the tail). Which fields change, and
   what must happen to `tail`?
3. Why is `append` O(1) here but O(n) if we dropped the `tail` field?
4. `remove(x)` returns `None` on a miss, but `remove_at(99)` raises. Why the
   asymmetry?
5. After removing the last remaining node, which three fields must all read
   "empty", and what goes wrong if `tail` isn't reset?
6. Walk the pointers for `prepend(0)` on an empty list. What gets set?

## Deep dive: common bugs

- **Losing the rest of the list.** Writing `prev.next = node` *before*
  `node.next = prev.next` discards the old continuation — everything after the
  insertion point becomes unreachable. Always rescue the old pointer first.

- **Forgetting to update `tail`.** Removing the tail without setting
  `tail = prev`, or emptying the list without `tail = None`, leaves `tail`
  pointing at a dead node. The next `append` corrupts the list silently. This is
  the bug `test_append_after_emptying_uses_tail` exists to catch.

- **Forgetting `length`.** Every insert must `+= 1` and every remove `-= 1`. A
  drifting `length` breaks the `index >= length` bounds checks, so valid indices
  start raising or invalid ones stop raising.

- **Off-by-one walking to `index - 1`.** For `insert_at`/`remove_at` in the
  middle you want the node *before* the target. Walking to `index` instead of
  `index - 1` splices in the wrong place.

- **Bad bounds operator.** Use `index >= length` for `get`/`remove_at` (last
  valid index is `length - 1`) but `index > length` for `insert_at` (inserting
  at `length` appends). Swapping them is a one-character bug with two failure
  modes.
