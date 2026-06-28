# Quick Sort

> sorting · stub: `src/topics/sorting/quick_sort.py` · test: `tests/test_quick_sort.py`
>
> 📚 Need more detail? See the [in-depth version](quick_sort.deep.md).

## Intuition
Pick one element as a "pivot", then shuffle the others so everything smaller
lands to its left and everything larger to its right. Now the pivot is in its
final sorted position, and you repeat the same trick on the left chunk and the
right chunk. Like sorting papers by repeatedly choosing a name and splitting the
pile into "before" and "after".

## How it works
This reference uses **Lomuto partition** on the **last element** as pivot, sorting
**in place** (`return None`). Use helpers `_quick_sort(arr, lo, hi)` and
`_partition(arr, lo, hi)`.

1. `_quick_sort(arr, lo, hi)`: if `lo >= hi`, the range has 0 or 1 items — return.
2. Partition `arr[lo..hi]` and get the pivot's final index `p`.
3. Recurse on `arr[lo..p-1]` and `arr[p+1..hi]`.
4. **Partition:** let `pivot = arr[hi]`. Keep a boundary `i = lo`. For each `j`
   from `lo` to `hi-1`, if `arr[j] <= pivot`, swap `arr[i], arr[j]` and `i += 1`.
5. Finally swap `arr[i], arr[hi]` to drop the pivot into place; return `i`.

Trace one partition of `[5, 2, 9, 1, 6]`, pivot = `6` (lo=0, hi=4):

```
j=0 arr[0]=5<=6 swap self, i->1 : [5, 2, 9, 1, 6]
j=1 arr[1]=2<=6 swap self, i->2 : [5, 2, 9, 1, 6]
j=2 arr[2]=9>6  skip             : [5, 2, 9, 1, 6]
j=3 arr[3]=1<=6 swap a[2],a[3] i->3: [5, 2, 1, 9, 6]
place pivot: swap a[3],a[4]      : [5, 2, 1, 6, 9]  -> p=3
then recurse on [5,2,1] and [9]
```

## Complexity
- **Time:** O(n log n) average; O(n^2) worst (already-sorted input with last-element
  pivot makes maximally unbalanced splits).
- **Space:** O(log n) average for the recursion stack (O(n) in the worst case).

Balanced partitions give log n depth times n work per level; degenerate pivots
collapse that to quadratic. Lomuto quicksort is **not stable** — swaps reorder
equal elements.

## Common pitfalls
- Forgetting to `return None` from the top-level `quick_sort`.
- Using `<` instead of `<=` in the partition: duplicates can break placement —
  the `[4, 4, 4, 4]` test guards this.
- Off-by-one bounds: the loop is `range(lo, hi)` (exclude the pivot), and you must
  swap the pivot in at `i` afterward.
- Recursing on `lo..p` instead of `lo..p-1` (the pivot is already placed) causes
  infinite recursion.
- Missing the `lo >= hi` base case overflows the stack on small ranges.

## Your task
Implement the function in `src/topics/sorting/quick_sort.py`, then run:

```bash
uv run pytest -k quick_sort
```

Peek at `solutions/quick_sort.py` only once you've given it a real attempt.
