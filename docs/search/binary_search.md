# Binary Search

> search · stub: `src/topics/search/binary_search.py` · test: `tests/test_binary_search.py`
>
> 📚 Need more detail? See the [in-depth version](binary_search.deep.md).

## Intuition
When the data is **sorted**, you can throw away half the remaining possibilities with a single comparison. Think of guessing a number between 1 and 100: you guess 50, get told "higher" or "lower," and instantly eliminate half the range. Repeat and you zero in fast.

## How it works
Keep a half-open window `[lo, hi)` — `lo` is the first index still in play, `hi` is one past the last.

1. Start with `lo = 0`, `hi = len(arr)`.
2. While `lo < hi`:
   - Compute `mid = (lo + hi) // 2`.
   - If `arr[mid] == target`, return `mid`.
   - If `arr[mid] < target`, the target must be to the right → `lo = mid + 1`.
   - Else it's to the left → `hi = mid`.
3. If the window empties (`lo == hi`), return `-1`.

Worked example — search for `7` in `[1, 3, 5, 7, 9, 11]`:

| step | lo | hi | mid | arr[mid] | compare to 7 | action       |
|------|----|----|-----|----------|--------------|--------------|
| 1    | 0  | 6  | 3   | 7        | equal        | **return 3** |

Search for `6` (absent): mid=3→7 (too big, hi=3); mid=1→3 (too small, lo=2); mid=2→5 (too small, lo=3); now `lo==hi==3` → window empty → `-1`.

## Complexity
- **Time:** O(log n)
- **Space:** O(1)

Each step halves the window, so it takes about log₂(n) steps; only a few index variables are stored.

## Common pitfalls
- Off-by-one in the window. With half-open `[lo, hi)`, use `hi = len(arr)`, loop while `lo < hi`, and set `hi = mid` (not `mid - 1`). Mixing this with inclusive `[lo, hi]` conventions causes infinite loops or skipped elements.
- Updating `lo = mid` instead of `lo = mid + 1` — `mid` was already checked, so reusing it can loop forever.
- Forgetting the empty list: `lo == hi == 0` makes the loop body never run, correctly returning `-1` — don't index before checking.
- Running it on **unsorted** data. Binary search is only valid on an ascending-sorted list.
- (FYI) Integer overflow on `mid` is a real bug in C/Java but **not** in Python — its ints are unbounded, so `(lo + hi) // 2` is fine.

## Your task
Implement the function in `src/topics/search/binary_search.py`, then run:

```bash
uv run pytest -k binary_search
```

Peek at `solutions/binary_search.py` only once you've given it a real attempt.
