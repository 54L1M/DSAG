# Hash Map (Separate Chaining)

> hashing · stub: `src/topics/hashing/map.py` · test: `tests/test_map.py`
>
> 📚 Need more detail? See the [in-depth version](map.deep.md).

## Intuition
A hash map stores key/value pairs and finds any of them in roughly constant time.
The trick: run the key through a `hash()` function to compute an array index, then
store the pair at that slot. It's like a coat-check: you hand over a coat (value),
get a ticket number (the hash), and that number tells the attendant exactly which
hook to grab later — no searching the whole rack.

Two coats can map to the same hook (a *collision*). We handle that by hanging a
small list on each hook and scanning just that short list.

## How it works
The map is an array of `capacity` buckets; each bucket is a list of `(key, value)`
pairs (this is **separate chaining**).

1. **Index a key:** `index = hash(key) % capacity`. With `capacity = 8`:
   - `hash("a") % 8` → say `3`
   - `hash("b") % 8` → say `3` too (collision!)
   - `hash("c") % 8` → say `6`

2. **`set(key, value)`** — go to the bucket, scan it. If the key is already there,
   overwrite its pair (do NOT add a second copy, do NOT bump `length`). Otherwise
   append the new pair and `length += 1`.

   ```
   bucket[3] -> [("a", 1), ("b", 2)]   # "a" and "b" collided, chained
   bucket[6] -> [("c", 3)]
   bucket[…] -> []
   ```

3. **`get(key)`** — index to the bucket, walk its short list, return the matching
   value or `None`.

4. **`remove(key)`** — index, find the pair, pop it, `length -= 1`, return the old
   value (or `None` if absent).

5. **Resize when crowded.** The *load factor* is `length / capacity`. When buckets
   get full, chains grow long and lookups slow down. After an insert, if
   `length > capacity * 0.75`, double `capacity` and **rehash every existing pair**
   into a fresh bucket array (indices change because `capacity` changed). The test
   `test_resize_keeps_all_entries` inserts 100 keys and checks all survive.

## Complexity
| Operation | Average | Worst case |
|-----------|---------|------------|
| `set`     | O(1) amortized | O(n) |
| `get`     | O(1)    | O(n) |
| `remove`  | O(1)    | O(n) |

Worst case is everything colliding into one bucket. A good `hash()` and resizing
keep chains short, so average stays O(1).
- **Space:** O(n)

## Common pitfalls
- **Update vs insert:** if the key already exists, overwrite in place — don't
  append a duplicate pair and don't increment `length`.
- **Forgetting to rehash on resize:** you can't just grow the array; every pair
  must be re-placed with `hash(k) % new_capacity` or `get` will look in the wrong
  bucket.
- **Returning the wrong thing:** `get`/`remove` must return `None` (not raise) for
  a missing key; `remove` returns the *old value*.
- **Mixing key types:** `1` and `"1"` are different keys (they hash differently) —
  the test relies on this.
- **Mutating while iterating** a bucket during remove — pop by index after finding.

## Your task
Implement the class in `src/topics/hashing/map.py`, then run:

```bash
uv run pytest -k map
```

Peek at `solutions/map.py` only once you've given it a real attempt.
