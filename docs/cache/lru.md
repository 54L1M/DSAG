# LRU Cache (Least Recently Used)

> cache · stub: `src/topics/cache/lru.py` · test: `tests/test_lru.py`
>
> 📚 Need more detail? See the [in-depth version](lru.deep.md).

## Intuition
An LRU cache holds a fixed number of items and, when it's full, throws away the
one you haven't touched in the longest time. Think of a desk: papers you just used
go on top of the pile, and when the desk overflows you toss whatever sank to the
bottom. Every time you read or write a paper, it goes back on top — so the bottom
is always the least-recently-used thing.

We want both "find a key fast" and "reorder by recency fast", so we combine two
structures: a dict for O(1) lookup and a doubly linked list for O(1) reordering.

## How it works
- **dict** `_lookup`: key → node (instant find).
- **doubly linked list**: `_head` = most recently used, `_tail` = least recently
  used. Each node has `prev`/`next` so we can detach it from the middle in O(1).

Helpers: `_prepend(node)` puts a node at the head; `_detach(node)` unlinks it;
`_evict()` detaches `_tail` and deletes it from the dict.

**`update(key, value)`**
1. If the key exists: overwrite its value, detach the node, prepend it (refresh
   recency). Done — `length` unchanged.
2. Else: make a node, add to dict, prepend, `length += 1`. If `length > capacity`,
   `_evict()` the tail.

**`get(key)`** returns the value and *also* moves the node to the head (a read
counts as a use). Missing key → `None`.

**Trace the test's a/b/c sequence (capacity 2):**
```
update("a",1)     list: a            (head=a, tail=a)
update("b",2)     list: b <-> a      (head=b, tail=a)
get("a") -> 1     list: a <-> b      (touching a moves it to head; tail=b)
update("c",3)     length 3 > 2 -> evict tail (b)
                  list: c <-> a      (b is gone)
get("b") -> None  (evicted)
get("a") -> 1     (survived because get refreshed it)
get("c") -> 3
```
This is `test_get_refreshes_recency`: the `get("a")` is what saves `a` and dooms
`b` instead.

## Complexity
| Operation | Big-O |
|-----------|-------|
| `get`     | O(1)  |
| `update`  | O(1)  |

The dict gives O(1) lookup; the linked list gives O(1) move-to-front and eviction.
- **Space:** O(n) for up to `capacity` nodes plus dict entries.

## Common pitfalls
- **`get` must refresh recency.** A read is a use — move the node to the head, or
  you'll evict items that are actually hot.
- **Updating an existing key must also refresh** (move to head) and overwrite the
  value, without changing `length`.
- **Evict the right end.** Drop the `_tail` (least recent), never the `_head`.
- **Linked-list bookkeeping:** when detaching, fix both neighbors' `prev`/`next`
  and update `_head`/`_tail` if you removed an end node — easy to leave a dangling
  pointer.
- **Off-by-one on capacity:** evict only after `length > capacity`, and remember to
  delete the evicted key from `_lookup` too (not just from the list).

## Your task
Implement the class in `src/topics/cache/lru.py`, then run:

```bash
uv run pytest -k lru
```

Peek at `solutions/lru.py` only once you've given it a real attempt.
