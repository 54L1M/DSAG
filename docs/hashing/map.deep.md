# Hash Map — In Depth

> In-depth companion · hashing · stub: `src/topics/hashing/map.py` · test: `tests/test_map.py`
>
> New here? Read the [quick version](map.md) first.

## The mental model
A hash map answers one question fast: "what value did I store under this key?"
A plain array already answers that for *integer* keys — `arr[5]` is one step. The
hash map's whole job is to turn *any* key (a string, a tuple, an int) into an
array index, so it can borrow that one-step lookup.

The translator is the hash function. `hash("apple")` returns some large, scrambled
integer. We squeeze it into a valid slot with the modulo operator:

```
index = hash(key) % capacity
```

`capacity` is how many slots (buckets) the underlying array has. So a key always
lands in the same slot — and to find it later we recompute the same index and look
there. That is the entire idea. Everything else (chaining, resizing) exists to keep
that lookup fast when reality gets messy.

In this build a bucket is not a single slot holding one pair. It is a *list* of
`(key, value)` pairs. The map is an array of such lists:

```
_buckets = [ [], [], [("a",1),("b",2)], [], [], [], [("c",3)], [] ]
              0   1         2            3   4   5      6        7
```

## Why it works — the invariant
Two invariants make every operation correct, and a third makes it fast.

1. **Placement invariant.** Every stored pair `(k, v)` lives in bucket
   `hash(k) % capacity`. `get`/`remove` recompute that index and are guaranteed to
   look in the right bucket. The moment this breaks (e.g. you grow the array but
   forget to recompute indices) entries become unreachable even though they still
   exist in memory.

2. **Uniqueness invariant.** A key appears at most once across all buckets. `set`
   enforces this by scanning the target bucket first: if the key is present it
   overwrites in place; only a genuinely new key is appended and only then is
   `length` incremented.

3. **Load-factor invariant (the speed guarantee).** The *load factor* is
   `length / capacity` — the average number of pairs per bucket. We keep it bounded
   by resizing whenever `length > capacity * 0.75`. Because the average chain length
   stays below a constant (~0.75), scanning a chain is constant work on average.
   That is *why* lookups are O(1) and not O(n).

## Detailed walkthrough
Collisions are unavoidable: infinitely many keys, finitely many buckets. Two keys
whose hashes land on the same index *collide*. There are two classic remedies.

- **Separate chaining (what we build).** Each bucket holds its own little list.
  Colliding keys just sit side by side in that list; lookup scans the short list.
- **Open addressing (what Python's real `dict` uses).** One pair per slot; on a
  collision you *probe* for another empty slot. The simplest probe is *linear
  probing*: try `index+1`, `index+2`, ... wrapping around. No side lists, better
  cache behavior, but trickier deletion (you can't just empty a slot or you break
  probe chains) and it degrades badly as the table fills. We use chaining because
  it is the clearer first lesson — but know that the standard library chose the
  other strategy.

Walk `set` from the reference design:

```python
bucket = self._buckets[hash(key) % self.capacity]
for i, (k, _v) in enumerate(bucket):
    if k == key:
        bucket[i] = (key, value)   # UPDATE in place — length unchanged
        return
bucket.append((key, value))        # INSERT — new key
self.length += 1
if self.length > self.capacity * 0.75:
    self._resize()
```

Notice the early `return` on update: it is what keeps `length` honest.

A resize doubles capacity and **rehashes** every pair into a fresh array. Indices
*must* be recomputed, because `% old_capacity` and `% new_capacity` generally give
different slots:

```python
def _resize(self):
    old = self._buckets
    self.capacity *= 2
    self._buckets = [[] for _ in range(self.capacity)]
    for bucket in old:
        for k, v in bucket:
            self._buckets[hash(k) % self.capacity].append((k, v))
```

ASCII before/after for a tiny `capacity = 4` map holding keys whose hashes are 3, 7,
11 (all `% 4 == 3`, a pile-up) once we double to 8:

```
capacity 4                     capacity 8 (rehashed)
0: []                          0: []
1: []                          1: []
2: []                          2: []
3: [h3, h7, h11]   ─resize→    3: [h3, h11]      (3%8=3, 11%8=3)
                               4: []
                               5: []
                               6: []
                               7: [h7]           (7%8=7)
```

The chain split apart, so future lookups in bucket 3 scan fewer items.

## Complexity, derived
Let `n = length`, `c = capacity`, load factor `α = n / c`.

**Average case.** A lookup costs: compute hash (O(1)) + scan one bucket. The
expected bucket length is `α`. Because resizing holds `α ≤ 0.75`, the scan is
expected constant work. So `get` and `remove` are **O(1) average**.

**`set` amortized.** A single `set` is O(1) average *except* on the resize step,
which is O(c) (rehash every pair). But resizes are rare: starting at capacity 8, a
resize happens after roughly every doubling of size. To insert `n` keys you resize
at sizes ~8, 16, 32, ..., n, and the total rehash work is
`8 + 16 + 32 + ... + n ≈ 2n` — a geometric series bounded by `2n`. Spread over `n`
inserts that is **O(1) amortized per insert**. This is the same accounting trick as
a dynamic array's doubling.

**Worst case.** If the hash function is adversarial or terrible, every key lands in
one bucket. Now a bucket *is* the whole dataset and every operation is **O(n)** — a
linear scan. A good `hash()` plus a bounded load factor is what keeps you out of
this hole. The 100-key resize test exercises the amortized path.

| Operation | Average | Worst |
|-----------|---------|-------|
| `set`     | O(1) amortized | O(n) |
| `get`     | O(1)    | O(n) |
| `remove`  | O(1)    | O(n) |

Space is O(n + c) = O(n).

## Edge cases in detail
- **Update an existing key** (`test_update_existing_key`): `set("a",1)` then
  `set("a",99)` must leave `length == 1` and return `99` on `get`. The scan-then-
  overwrite path does this; an accidental append would double-count.
- **Missing key** (`test_missing_key_returns_none`): `get("nope")` returns `None`,
  never raises. The scan falls through the loop and returns `None`.
- **Remove returns the old value, then None** (`test_remove`): first `remove("a")`
  returns `1` and drops `length` to 0; a second `remove("a")` returns `None`.
- **Resize keeps all 100 entries** (`test_resize_keeps_all_entries`): inserting
  `0..99` forces several doublings; every key must still resolve. This passes only
  if rehashing is correct.
- **`1` vs `"1"` are different keys** (`test_integer_and_string_keys`): they compare
  unequal (`1 != "1"`) and generally hash differently, so they occupy independent
  entries even if they ever shared a bucket.
- **Hash of an int.** In CPython `hash(small_int) == small_int`, so integer keys
  index very predictably — handy when reasoning, but don't rely on it for behavior.

## Variations & trade-offs
- **Chaining vs open addressing** — discussed above. Chaining tolerates high load
  factors gracefully; open addressing is more memory-compact and cache-friendly but
  needs careful deletion (tombstones) and a stricter load-factor ceiling.
- **Load-factor threshold.** 0.75 is a common balance. Lower (e.g. 0.5) means
  fewer collisions but more memory and more frequent resizes; higher means denser
  tables and longer chains.
- **Growth factor.** Doubling keeps amortized inserts O(1). Growing by a fixed
  amount instead would make resizes frequent and inserts O(n) amortized.
- **Negative hashes.** Python's `%` always returns a non-negative result for a
  positive modulus (`-5 % 8 == 3`), so `hash(key) % capacity` is always a valid
  index. In languages where `%` can go negative you would mask or add `capacity`.

## Connections
- `../linear/array_list.md` — a bucket array that doubles and copies is exactly a
  dynamic array; the resize amortization argument is the same geometric series.
- `../cache/lru.md` — the LRU cache uses a dict (this structure) for its O(1)
  lookups, paired with a linked list for ordering.
- `../trie/trie.md` — trie nodes often keep their children in a dict keyed by
  character, i.e. a hash map nested at every node.

## Self-check
1. Why does `set` scan the bucket *before* appending, and what breaks if it
   doesn't?
2. After doubling `capacity`, why can't you keep pairs in their old buckets?
3. Derive why `n` inserts cost O(n) total rather than O(n·log n) or O(n²).
4. What single property of the hash function turns every operation into O(n)?
5. The map stores `1` and `"1"`. They land in the same bucket. How does `get(1)`
   still return the right value?
6. If you raised the resize threshold from 0.75 to 5.0, what would happen to lookup
   time and memory?

## Deep dive: common bugs
- **Counting an update as an insert.** Forgetting the early `return` after an
  in-place overwrite appends a duplicate pair *and* bumps `length`. Now `get` may
  return the stale first copy, and `length` over-reports. `test_update_existing_key`
  catches this.
- **Resizing without rehashing.** Growing `_buckets` but leaving pairs where they
  were means `get` computes `hash(k) % new_capacity` and looks in a bucket the pair
  was never moved to — entries silently vanish. `test_resize_keeps_all_entries` is
  designed to fail loudly here.
- **Resizing at the wrong moment.** Check the threshold *after* incrementing
  `length` on a real insert, not on an update (which doesn't grow the map).
- **Mod sign / zero capacity.** Guard `capacity >= 1` (the solution uses
  `max(1, capacity)`) so `% capacity` never divides by zero. Don't hand-roll
  `abs(hash(key)) % capacity` thinking Python needs it — Python's `%` already
  yields a valid index for negative hashes.
- **Mutating a bucket while iterating it.** In `remove`, find the index first, then
  `pop(i)` and return — don't delete inside a `for x in bucket` loop.
- **Comparing only by hash.** Two distinct keys can share a hash. Always compare
  with `k == key`, never "same hash means same key".
