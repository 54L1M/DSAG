# Merge Sort

> sorting · stub: `src/topics/sorting/merge_sort.py` · test: `tests/test_merge_sort.py`
>
> 📚 Need more detail? See the [in-depth version](merge_sort.deep.md).

## Intuition
Split the deck in half, hand each half to a friend to sort, then zip the two
sorted halves back together by repeatedly taking whichever front card is smaller.
Because each half is already sorted, merging is a single clean pass. This
divide-and-conquer split keeps halving until each piece is trivially sorted.

## How it works
1. Base case: a list of length 0 or 1 is already sorted — return a copy of it.
2. Split at the middle: `mid = len(arr) // 2`, giving `arr[:mid]` and `arr[mid:]`.
3. Recursively `merge_sort` each half, getting back two sorted lists.
4. **Merge:** walk both with indices `i`, `j`; append the smaller front element
   (`left[i] <= right[j]` keeps it stable), then drain whatever remains.
5. This builds and returns a **new** list — it does not sort in place, and the
   original `arr` is left unchanged.

Trace on `[5, 2, 9, 1, 6]`:

```
split : [5, 2]        and [9, 1, 6]
        [5][2]            [9] and [1, 6] -> [1][6]
merge : [2, 5]            [1, 6] then [1, 6, 9]
final : merge [2, 5] + [1, 6, 9]
        take 1,2,5,6,9 -> [1, 2, 5, 6, 9]
```

## Complexity
- **Time:** O(n log n) in all cases (best, average, worst) — the depth of splits
  is log n and each level merges n items.
- **Space:** O(n).

The guaranteed O(n log n) and the extra O(n) buffers are the trade-off versus
quicksort. Merge sort is **stable**: using `<=` when comparing fronts means equal
elements keep their original order.

## Common pitfalls
- Returning `None` or sorting in place — this contract returns a **new** list.
- Returning `arr` directly in the base case can alias the input; return a copy
  (`list(arr)`) so callers never see mutation.
- Forgetting to drain the leftover tail of one side after the merge loop ends.
- Using `<` instead of `<=` in the merge breaks stability.
- A bad split (e.g. `arr[:mid]` and `arr[mid+1:]`) drops an element and recurses
  forever or loses data.

## Your task
Implement the function in `src/topics/sorting/merge_sort.py`, then run:

```bash
uv run pytest -k merge_sort
```

Peek at `solutions/merge_sort.py` only once you've given it a real attempt.
