# ArrayList (dynamic array) — In Depth

> In-depth companion · linear · stub: `src/topics/linear/array_list.py` · test: `tests/test_array_list.py`
>
> New here? Read the [quick version](array_list.md) first.

## The mental model

An ArrayList is the opposite philosophy from a linked list. Instead of scattered
nodes joined by pointers, it stores elements **contiguously** in a fixed-size
backing buffer, and tracks how many slots are actually in use.

```
buffer (capacity 4):  [ a | b | c | _ ]
                        0   1   2   3
length = 3            ^^^^^^^^^^^   ^ spare slot (holds None)
                      in use        unused
```

Three fields tell the whole story:

- `_data` — the backing buffer, a fixed-size list pre-filled with `None`.
- `length` — how many slots are actually live (the logical size).
- `capacity` — how big the buffer is (the physical size).

The key idea: **`capacity` ≥ `length`**, and we keep spare slots so that most
`push`es are just "drop the value in slot `length`, bump `length`." Only when the
buffer fills do we allocate a bigger one and copy over — that occasional copy is
what makes `push` *amortized* O(1) rather than true O(1).

Because the buffer is contiguous and indices map directly to memory offsets,
`get`/`set` are real O(1) random access — the thing a linked list can never do.

## Why it works — the invariant

1. **`0 ≤ length ≤ capacity`** at all times.
2. **Live data lives in `_data[0:length]`**; everything in `_data[length:]` is
   `None` (unused). This is why `pop`/`remove_at` must *None-out* the vacated
   slot — to keep the dead region clean and let Python release the object.
3. **`capacity == len(_data)`** — the bookkeeping number matches the real buffer.
4. **Emptiness is `length == 0`**, *not* "the buffer looks empty." The buffer is
   never truly empty (it's full of `None` padding), so you must trust `length`.

That last point is the whole ballgame for correctness, and the source of the
nastiest bug (see falsy values, below).

## Detailed walkthrough

**`get`/`set(index)` — O(1).** Bounds-check `0 ≤ index < length`, then index the
buffer directly. Note the bound is `length`, not `capacity` — index 3 in the
diagram above is out of range even though the slot physically exists.

```python
def get(self, index):
    if index < 0 or index >= self.length:
        raise IndexError(index)
    return self._data[index]
```

**`push(item)` — amortized O(1).** Ensure room for one more, drop the value at
slot `length`, bump `length`.

```
push d into [ a | b | c | _ ] (len 3, cap 4):
  room available -> [ a | b | c | d ]  len 4, cap 4

push e (len 4, cap 4 -> full!):
  grow: new buffer cap 8, copy a,b,c,d over
  [ a | b | c | d | _ | _ | _ | _ ]
  drop e -> [ a | b | c | d | e | _ | _ | _ ]  len 5, cap 8
```

The growth routine `_ensure_capacity(needed)` doubles until the buffer is big
enough, allocates a fresh list, and copies the live elements:

```python
def _ensure_capacity(self, needed):
    if needed <= self.capacity:
        return
    new_cap = self.capacity
    while new_cap < needed:
        new_cap *= 2
    new_data = [None] * new_cap
    for i in range(self.length):
        new_data[i] = self._data[i]   # copy must happen on resize
    self._data = new_data
    self.capacity = new_cap
```

**`pop()` — O(1).** Empty (`length == 0`) → return `None`. Otherwise decrement
`length`, read the now-last slot, **None it out**, and return it.

```
pop from [ a | b | c | _ ] (len 3):
  length -> 2
  value = _data[2] = c
  _data[2] = None        <- critical: release the slot
  [ a | b | _ | _ ]  len 2
  return c
```

**`insert_at(item, index)` — O(n).** `index == length` appends; `index > length`
raises. Ensure capacity, then shift everything from the end down to `index` one
slot **right**, walking high-to-low so you don't overwrite unread data:

```
insert X at index 1 into [ a | b | c | _ ] (len 3):
  ensure room (len+1=4 fits cap 4)
  shift right, high->low:
    _data[3] = _data[2]   [ a | b | c | c ]
    _data[2] = _data[1]   [ a | b | b | c ]
  place: _data[1] = X     [ a | X | b | c ]  len 4
```

**`remove_at(index)` — O(n).** Bounds-check, save the value, shift everything
after `index` one slot **left** (low-to-high this time), decrement `length`, and
None-out the now-stale last slot:

```
remove index 1 from [ a | b | c | d ] (len 4):
  value = b
  shift left, low->high:
    _data[1] = _data[2]   [ a | c | c | d ]
    _data[2] = _data[3]   [ a | c | d | d ]
  length -> 3
  _data[3] = None         [ a | c | d | _ ]
  return b
```

## Complexity, derived

| Operation     | Time            | Why |
|---------------|-----------------|-----|
| `get` / `set` | O(1)            | Direct index into contiguous memory. |
| `push`        | amortized O(1)  | Usually one write; occasionally an O(n) resize. |
| `pop`         | O(1)            | Truncate and None-out the last slot. |
| `insert_at`   | O(n)            | Shift up to `n` elements right. |
| `remove_at`   | O(n)            | Shift up to `n` elements left. |
| `length`      | O(1)            | Stored. |

**Why is `push` amortized O(1) and not O(n)?** Most pushes are a single write.
The expensive part is the copy on resize — but resizes get *rarer* as the list
grows, because doubling makes the gap between resizes grow too. Count the total
copy work to grow from 1 to n by doubling: you copy 1, then 2, then 4, then 8,
…, up to n elements:

```
1 + 2 + 4 + 8 + ... + n
```

This geometric series sums to `2n − 1 < 2n`. So **n pushes cost at most ~2n
copies total** — that's a constant (≈2) per push on average. Spread the rare
expensive resizes across the many cheap pushes and each push is O(1)
*amortized*. (If you grew by a *fixed* amount instead of doubling, the series
would be `k + 2k + 3k + … ≈ n²/2k`, i.e. O(n) per push — doubling is what saves
you.)

## Edge cases in detail

- **Falsy values must round-trip** (`test_falsy_values_roundtrip`). Push `0`
  twice, then `pop()` must return `0`. This is the trap: emptiness is
  `length == 0`, **never** a truthiness test on a stored value. Code like:

  ```python
  def pop(self):
      value = self._data[self.length - 1]
      if not value:          # BUG: 0, "", [], False all look "empty"
          return None
      ...
  ```

  treats a legitimately-stored `0` (or `""`, `[]`, `False`) as "nothing here"
  and returns `None`. The correct guard is `if self.length == 0:`. This is the
  single most important lesson the test enforces: **distinguish "no value" from
  "a falsy value."**

- **Many doublings** (`test_push_get`). Pushing 10 items into a capacity-2 list
  forces resizes 2→4→8→16. Every element must survive each copy intact — if
  `_ensure_capacity` copies the wrong range or forgets to reassign `_data`, the
  reread fails.

- **Out-of-range raises** (`test_out_of_range_raises`). `get`/`set`/`remove_at`
  use `index >= length`; `insert_at` uses `index > length` (inserting *at*
  `length` is the append case). Same boundary rules as the linked lists.

- **Insert/remove at the ends.** `insert_at(x, length)` appends (the shift loop
  runs zero times). `remove_at(length-1)` removes the last (shift loop runs zero
  times, then None-out). The loops naturally degenerate — no special-casing
  needed.

- **Pop on empty** returns `None`, no exception — consistent with stack/queue.

## Variations & trade-offs

- **Array vs. linked list.** Contiguous memory gives the ArrayList O(1) random
  access and excellent cache locality (the CPU prefetches neighbors). The cost:
  inserting/removing in the middle shifts O(n) elements, and growth needs
  occasional O(n) copies. A [linked list](../linked_lists/singly_linked_list.deep.md)
  flips it — O(1) splices, but O(n) access and pointer-chasing that thrashes the
  cache. Rule of thumb: arrays for read-heavy / index-heavy work, linked lists
  for insert/remove-heavy work where you already hold the position.

- **Growth factor.** Doubling (×2) is common; some libraries use ×1.5 to waste
  less memory at the cost of more frequent copies. Both keep `push` amortized
  O(1); only the constant changes.

- **Shrinking.** This implementation never shrinks `capacity` on `pop`.
  Production arrays sometimes halve the buffer when it's, say, ¼ full — but you
  must shrink at a *different* threshold than you grow, or alternating
  push/pop at the boundary causes thrashing (resize on every call).

## Connections

- An ArrayList is the natural backing store for an array-based
  [Stack](stack.deep.md) (push = append, pop = truncate).
- The same "fixed buckets + resize when too full" idea powers a hash map: see
  [map](../hashing/map.md), where the buckets array grows and rehashes once the
  load factor crosses a threshold — the doubling logic here is the direct
  ancestor of that resize.
- Python's built-in `list` *is* a dynamic array doing exactly this under the
  hood; you're reimplementing CPython's growth strategy by hand.

## Self-check

1. Why is the in-range bound `index < length` and not `index < capacity`?
2. Walk the geometric series that proves `push` is amortized O(1). What does the
   sum `1+2+4+…+n` equal, and why does that give O(1) per push?
3. Why must `pop` and `remove_at` set the vacated slot back to `None`?
4. Why does `insert_at` shift high-to-low but `remove_at` shift low-to-high?
5. Push `0`, push `0`, then `pop()`. What must it return, and what wrong
   emptiness check would break it?
6. Why does `_ensure_capacity` have to allocate a *new* buffer and copy, rather
   than extending the old one in place?

## Deep dive: common bugs

- **Truthiness instead of length for emptiness.** Using `if not value` /
  `if not self._data[i]` to detect "empty" swallows legitimately-stored falsy
  values (`0`, `""`, `[]`, `False`). Always gate on `self.length == 0`. This is
  the bug `test_falsy_values_roundtrip` is built to catch.

- **Forgetting to None-out the popped/removed slot.** Leaving the old object in
  `_data[length:]` keeps it alive (a memory leak) and pollutes the dead region,
  so any logic that scans the buffer sees stale ghosts.

- **Not copying on resize.** Allocating a bigger buffer but forgetting to copy
  the live elements over (or reassign `self._data` / `self.capacity`) loses all
  data. The 10-push test catches this immediately.

- **Wrong shift direction.** Shifting low-to-high on an *insert* overwrites the
  element you haven't moved yet, smearing one value across the gap. Inserts must
  shift high-to-low; removes must shift low-to-high.

- **Off-by-one in shift ranges.** `insert_at` copies `_data[i] = _data[i-1]` for
  `i` from `length` down to `index+1`; `remove_at` copies `_data[i] = _data[i+1]`
  for `i` from `index` up to `length-2`. A wrong endpoint duplicates or drops an
  element.

- **Bounds operator mix-up.** `index >= length` for get/set/remove_at, but
  `index > length` for insert_at (append is allowed). Swapping them breaks the
  append case or lets a bad index through.

- **Forgetting `length` bookkeeping.** Every `push`/`insert_at` `+= 1`, every
  `pop`/`remove_at` `-= 1`. Drift here corrupts every bounds check and the
  emptiness test at once.
