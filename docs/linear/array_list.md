# ArrayList (dynamic array)

> linear · stub: `src/topics/linear/array_list.py` · test: `tests/test_array_list.py`
>
> 📚 Need more detail? See the [in-depth version](array_list.deep.md).

## Intuition

An array list gives you index-based access (`get`/`set` in O(1)) *and* the ability
to grow without limit. The trick: keep a fixed-size **backing buffer** with some
spare slots, and when it fills up, allocate a bigger one and copy everything over.
Think of a **theatre that books out**: when the hall is full you move the whole
audience into a hall with twice the seats. Python's `list` already does this for
you — the lesson is to implement the growth strategy by hand.

## How it works

Internals: a backing list `_data` pre-sized to `capacity` (filled with `None`), a
`length` counter (how many slots are actually used), and `capacity` (how many
exist). The slots from `length` to `capacity - 1` are spare.

```
length = 3, capacity = 4
_data = [ a , b , c , None ]
          0   1   2    3
          \_______/    \__ spare
            used
```

**push(d)** — fits, so drop it at index `length` and bump the counter:

```
_data = [ a , b , c , d ]      length = 4, capacity = 4   (now full)
```

**push(e)** — buffer is full → **double the capacity and copy**, then place:

```
new _data = [ a , b , c , d , None, None, None, None ]   capacity 4 -> 8
_data[4] = e                                              length = 5
```

This copy is O(n), but it only happens after the buffer doubles, so it is rare —
that is why `push` is **amortized O(1)** (cheap on average across many pushes).

**insert_at(item, i)** — shift every element from the end down to `i` one slot to
the **right** (iterate high → low so you don't overwrite), then drop `item` at `i`:

```
insert_at(x, 1) into [a, b, c]:
  _data[3] = _data[2]   # c
  _data[2] = _data[1]   # b
  _data[1] = x          # -> [a, x, b, c]
```

**remove_at(i)** — return `_data[i]`, then shift later elements one slot **left**
(iterate low → high), decrement `length`, and clear the now-unused trailing slot
to `None`.

## Complexity

| Operation     | Big-O          | Why                                    |
| ------------- | -------------- | -------------------------------------- |
| `get` / `set` | O(1)           | direct index into the buffer           |
| `push`        | amortized O(1) | O(n) only on the occasional doubling   |
| `pop`         | O(1)           | drop the last element                  |
| `insert_at`   | O(n)           | shift the tail right                   |
| `remove_at`   | O(n)           | shift the tail left                    |

- **Space:** O(n) (up to ~2x the live elements, because of spare capacity)

## Common pitfalls

- **Distinguish `length` from `capacity`.** Bounds checks use `length` (the live
  count); the buffer size is `capacity`. Mixing them lets you read spare `None`s.
- **Grow *before* writing.** Call your `_ensure_capacity` check at the start of
  `push` and `insert_at`, then copy old → new buffer and update `capacity`.
- **Shift in the right direction/order.** Insert shifts right and must iterate
  from high index down; remove shifts left and iterates low up. Wrong order
  clobbers values.
- **Don't test truthiness for "empty slot."** `0`, `""`, and `False` are valid
  stored values — track emptiness with `length`, never `if _data[i]:`.
  `test_falsy_values_roundtrip` pushes `0` to catch this.
- **Bounds rules:** `get`/`set`/`remove_at` valid for `0 <= index < length`;
  `insert_at` allows `index == length` (append) but raises for `index > length`.

## Your task

Implement the class in `src/topics/linear/array_list.py`, then run:

```bash
uv run pytest -k array_list
```

Peek at `solutions/array_list.py` only once you've given it a real attempt.
