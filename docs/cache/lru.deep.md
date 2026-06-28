# LRU Cache — In Depth

> In-depth companion · cache · stub: `src/topics/cache/lru.py` · test: `tests/test_lru.py`
>
> New here? Read the [quick version](lru.md) first.

## The mental model
An LRU (Least Recently Used) cache is a fixed-size box. While there's room, every
new item just goes in. Once it's full and you add one more, it throws out the item
you've touched *least recently* — the assumption being that what you used recently,
you'll use again soon (temporal locality).

So the cache must do two different things fast, on every single operation:

1. **Find a key by name** — "is `b` in here, and what's its value?"
2. **Reorder by recency** — "I just used `b`, mark it as the freshest; whatever's
   stalest is the eviction candidate."

No single structure does both in O(1). That tension is the whole design.

## Why it works — the invariant
The cache pairs two structures, each covering the other's weakness:

- A **dict** `_lookup: key -> node` gives O(1) *find*. But a dict has no notion of
  "which key is stale" — it can't order by recency.
- A **doubly linked list** of nodes gives O(1) *reorder*: detach a node from the
  middle and splice it to the front in constant time, because each node knows its
  `prev` and `next`. But a list alone can't find a key without an O(n) walk.

Use both and you get O(1) find *and* O(1) reorder. The dict's values are the very
same node objects living in the list — one node, two ways to reach it.

Invariants held between operations:

1. **List order = recency order.** `_head` is the most-recently-used node, `_tail`
   the least. Every `get`/`update` moves the touched node to the head.
2. **Dict mirrors the list.** `key in _lookup` ⇔ a node for `key` is in the list,
   and `_lookup[key]` *is* that node. `length == len(_lookup)` == node count.
3. **Capacity bound.** After any `update`, `length ≤ capacity` (eviction restores
   this).

Because the freshest is always at the head and the stalest at the tail, eviction is
just "drop the tail" — O(1), no searching.

## Detailed walkthrough
Each node carries its key, its value, and two pointers:

```
class _Node:        key  value  prev  next
```

(The node stores its own `key` so that when we evict the tail we know which dict
entry to delete.) The list, drawn most-recent → least-recent:

```
        _head                         _tail
          |                             |
          v                             v
   None <- [b|2] <-> [a|1] <-> [c|3] -> None
            prev/next pointers link neighbors both ways
```

Two helpers do all the pointer surgery:

```python
def _prepend(self, node):          # put node at the head (most recent)
    node.prev = None
    node.next = self._head
    if self._head is not None:
        self._head.prev = node
    self._head = node
    if self._tail is None:         # list was empty -> node is also the tail
        self._tail = node

def _detach(self, node):           # unlink node, fixing both neighbors + ends
    if node.prev is not None: node.prev.next = node.next
    else:                     self._head = node.next      # was the head
    if node.next is not None: node.next.prev = node.prev
    else:                     self._tail = node.prev      # was the tail
    node.prev = node.next = None
```

"Move to front" is then just `_detach(node)` followed by `_prepend(node)`. `get`
and the update-existing path both reduce to exactly that.

```python
def update(self, key, value):
    node = self._lookup.get(key)
    if node is not None:           # existing key: overwrite + refresh
        node.value = value
        self._detach(node); self._prepend(node)
        return                     # length unchanged
    node = _Node(key, value)       # new key
    self._lookup[key] = node
    self._prepend(node)
    self.length += 1
    if self.capacity > 0 and self.length > self.capacity:
        self._evict()              # detach tail + del from dict + length -= 1

def get(self, key):
    node = self._lookup.get(key)
    if node is None: return None
    self._detach(node); self._prepend(node)   # a read is a use
    return node.value
```

### Trace the test sequence (capacity 2)
This is `test_get_refreshes_recency`, where the `get` is the load-bearing move:

```
update("a",1)     list: a               (head=a, tail=a)         length 1
update("b",2)     list: b <-> a         (head=b, tail=a)         length 2
get("a") -> 1     detach a, prepend a
                  list: a <-> b         (head=a, tail=b)         length 2
update("c",3)     new key: prepend c -> length 3 > capacity 2
                  evict tail (b): detach b, del _lookup["b"]
                  list: c <-> a         (head=c, tail=a)         length 2
get("b") -> None  ("b" was evicted)
get("a") -> 1     ("a" survived — the get above made it fresh)
get("c") -> 3
```

Without the recency refresh inside `get`, `a` would still be the tail and `update("c")`
would evict `a` instead of `b`. The single `get("a")` is what flips their fates.

## Complexity, derived
- **`get`**: one dict lookup (O(1) average — see `../hashing/map.md`) + `_detach` +
  `_prepend`. Each helper touches a fixed number of pointers regardless of size →
  **O(1)**.
- **`update`**: one dict lookup, then either overwrite+move (O(1)) or
  insert+maybe-evict. Eviction is `_detach(tail)` + one `del` from the dict + a
  decrement — all O(1). So **O(1)** overall.

There is no loop over the data in either operation. That constant-time guarantee is
the entire reason for the dict+list combo; either structure alone would force an
O(n) step somewhere. Space is O(capacity).

## Edge cases in detail
- **Missing key** (`test_missing_key_returns_none`): `get("x")` with `x` absent
  returns `None` and changes nothing.
- **`get` refreshes recency** (`test_get_refreshes_recency`): traced above — a read
  moves the node to the head and can change who gets evicted next.
- **Update existing key refreshes *and* overwrites**
  (`test_update_existing_refreshes_and_overwrites`): `update("a",10)` sets the value
  to 10, moves `a` to the head, and leaves `length` unchanged; the later
  `update("c")` then evicts `b` (the tail), not `a`.
- **Eviction picks the tail** (`test_evicts_least_recently_used`): after `a, b, c`
  with no reads, `a` is the tail and is the one dropped.
- **First insert**: list is empty, so `_prepend` sets both `_head` and `_tail` to
  the new node.
- **Capacity 0**: the `capacity > 0` guard means a 0-capacity cache effectively
  stores nothing useful — anything inserted exceeds capacity. (Real designs often
  reject capacity 0 outright; here it simply never holds an item past one insert.)

## Variations & trade-offs
- **`collections.OrderedDict`**: gives `move_to_end` and `popitem(last=False)`,
  which implement an LRU in a few lines — it *is* a dict+linked-list under the hood.
  Building the list by hand is the lesson; use `OrderedDict` in real code.
- **`functools.lru_cache`**: a ready-made memoization decorator built on the same
  idea — caches function results, evicting LRU when full.
- **LFU (Least *Frequently* Used)**: evicts by access *count* rather than recency.
  Better when some keys are perennially popular; needs frequency counters and is
  fiddlier to keep O(1).
- **Sentinel/dummy head & tail nodes**: a common variant adds two never-removed
  guard nodes so `_prepend`/`_detach` never special-case `None` ends. This build
  instead checks for `None`; the sentinel version trades a bit of memory for fewer
  branches.

## Connections
- `../hashing/map.md` — `_lookup` is a hash map; its O(1) average lookup is what
  makes the cache's "find" step O(1). The cache inherits the hash map's average-case
  caveat.
- `../linear/doubly_linked_list.md` — the recency list is a doubly linked list; the
  `_detach`/`_prepend` pointer surgery is the same splice/unsplice you practice
  there, reused for a real purpose.

## Self-check
1. Why can't a dict alone implement an LRU cache? Why can't a linked list alone?
2. What exactly does "move to front" decompose into, and why is it O(1)?
3. Why must `get` reorder the list, not just return the value?
4. When updating an *existing* key, why does `length` stay the same?
5. In the a/b/c trace, which single operation decides that `b` (not `a`) is evicted,
   and why?
6. Why does each node store its own `key`? What breaks at eviction time without it?

## Deep dive: common bugs
- **`get` doesn't refresh recency.** The most common LRU bug: returning the value
  but leaving the node where it was. Hot keys then drift to the tail and get
  evicted. `test_get_refreshes_recency` is built to catch exactly this.
- **Evicting the wrong end.** Dropping `_head` (most recent) instead of `_tail`
  (least recent) throws out your freshest data. Eviction is always tail-side.
- **Update-existing forgets to refresh.** Overwriting the value but not moving the
  node to the head leaves recency stale; the key may be wrongly evicted next.
  `test_update_existing_refreshes_and_overwrites` checks both halves.
- **Forgetting to delete from the dict on eviction.** Detaching the tail node but
  leaving `_lookup[key]` behind breaks invariant 2: `length`/dict drift apart and a
  later `get` returns a node no longer in the list. Always `del _lookup[node.key]`.
- **Pointer surgery mistakes in `_detach`.** Must handle four cases: node is head,
  node is tail, node is both (only element), node is in the middle. Miss the "is it
  an end?" check and you leave `_head`/`_tail` dangling at a removed node.
- **Off-by-one on capacity.** Evict only when `length > capacity` (strictly
  greater), checked *after* incrementing on a new insert — not on an update, which
  doesn't grow the cache.
