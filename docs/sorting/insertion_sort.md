# Insertion Sort

> sorting · stub: `src/topics/sorting/insertion_sort.py` · test: `tests/test_insertion_sort.py`
>
> 📚 Need more detail? See the [in-depth version](insertion_sort.deep.md).

## Intuition
This is how most people sort a hand of playing cards: keep the cards on the left
already in order, pick up the next card, and slide it leftward until it sits in
the right spot. The sorted region grows one element at a time until it covers the
whole list.

## How it works
1. Treat `arr[0]` alone as a sorted prefix of length 1.
2. For each `i` from 1 onward, save `key = arr[i]`.
3. Walk backward from `j = i - 1`: while `arr[j] > key`, copy `arr[j]` one slot
   to the right (`arr[j+1] = arr[j]`) to open a gap.
4. When you hit something `<= key` (or fall off the left edge), drop `key` into
   the gap: `arr[j+1] = key`.
5. All shifts happen **in place** — you mutate `arr` and `return None`.

Trace on `[5, 2, 9, 1, 6]` (`|` marks end of the sorted prefix):

```
start : [5 | 2, 9, 1, 6]
i=1   : [2, 5 | 9, 1, 6]   # 2 shifted past 5
i=2   : [2, 5, 9 | 1, 6]   # 9 already in place
i=3   : [1, 2, 5, 9 | 6]   # 1 slid all the way left
i=4   : [1, 2, 5, 6, 9 |]  # 6 inserted before 9
```

## Complexity
- **Time:** O(n^2) worst (reverse-sorted); O(n) best (already sorted — the inner
  loop never runs).
- **Space:** O(1).

Each element may shift past the entire sorted prefix, hence quadratic in the
worst case; but on nearly-sorted data it is close to linear. It is stable since
the shift condition is strictly `>`.

## Common pitfalls
- Forgetting to `return None` — returning the list fails the in-place test.
- Off-by-one on the final placement: it is `arr[j+1] = key`, not `arr[j] = key`,
  because `j` ends one slot left of the gap.
- Using `arr[j] >= key` shifts equal elements and breaks stability.
- Overwriting `arr[i]` before saving it into `key`, losing the value you wanted
  to insert.
- Letting `j` go below 0 in the index without guarding `j >= 0` first.

## Your task
Implement the function in `src/topics/sorting/insertion_sort.py`, then run:

```bash
uv run pytest -k insertion_sort
```

Peek at `solutions/insertion_sort.py` only once you've given it a real attempt.
