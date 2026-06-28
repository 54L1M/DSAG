# Bubble Sort

> sorting · stub: `src/topics/sorting/bubble_sort.py` · test: `tests/test_bubble_sort.py`
>
> 📚 Need more detail? See the [in-depth version](bubble_sort.deep.md).

## Intuition
Walk through the list comparing each pair of neighbours, and swap them whenever
the left one is bigger than the right one. Like air bubbles rising in water, the
largest value floats to the far end on each pass. Repeat passes until nothing
needs swapping anymore.

## How it works
1. Make a pass from left to right over the list.
2. Compare each adjacent pair `arr[j]` and `arr[j+1]`; if out of order, swap.
3. After pass `i`, the largest `i` items are parked at the end, so the next pass
   can stop one element earlier.
4. If a whole pass makes zero swaps, the list is already sorted: stop early.
5. The work is **in place** — you mutate `arr` directly and `return None`.

Trace on `[5, 2, 9, 1, 6]` (showing the list after each full pass):

```
start : [5, 2, 9, 1, 6]
pass 1: [2, 5, 1, 6, 9]   # 9 bubbled to the end
pass 2: [2, 1, 5, 6, 9]   # 6 settled
pass 3: [1, 2, 5, 6, 9]   # sorted
pass 4: [1, 2, 5, 6, 9]   # no swaps -> early exit
```

## Complexity
- **Time:** O(n^2) average and worst; O(n) best (already sorted, thanks to the
  early-exit flag).
- **Space:** O(1).

Every pair may need comparing on every pass, giving the quadratic cost. It is
stable (equal elements keep their relative order) since it only swaps on strictly
greater-than.

## Common pitfalls
- Forgetting to `return None` — returning the list fails the in-place test.
- Looping `j` over the whole list each pass instead of `n - 1 - i`, causing an
  index error at `arr[j+1]` or wasted work.
- Comparing with `>=` instead of `>`, which swaps equal elements and breaks
  stability (and loops forever if you also loop on no-progress).
- Dropping the `swapped` flag — correct, but you lose the O(n) best case.
- Building a new list instead of swapping in place.

## Your task
Implement the function in `src/topics/sorting/bubble_sort.py`, then run:

```bash
uv run pytest -k bubble_sort
```

Peek at `solutions/bubble_sort.py` only once you've given it a real attempt.
