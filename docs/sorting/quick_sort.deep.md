# Quick Sort — In Depth

> In-depth companion · sorting · stub: `src/topics/sorting/quick_sort.py` · test: `tests/test_quick_sort.py`
>
> New here? Read the [quick version](quick_sort.md) first.

## The mental model

Quick sort is divide-and-conquer like merge sort, but it does the hard work
*before* recursing instead of after. Pick one element as the **pivot**. Rearrange
the range so that everything `<= pivot` is to its left and everything `> pivot` is
to its right. After this *partition*, the pivot is sitting in its **final sorted
position** — it will never move again. Now recurse into the left chunk and the
right chunk independently. There is no "combine" step: once both sides are sorted,
the whole range is sorted, for free.

This repo uses the **Lomuto partition scheme** with the **last element as pivot**,
sorting **in place** (`return None`). The structure is two helpers:

```python
def quick_sort(arr):
    _quick_sort(arr, 0, len(arr) - 1)      # public: returns None

def _quick_sort(arr, lo, hi):
    if lo >= hi: return                    # 0 or 1 elements: done
    p = _partition(arr, lo, hi)            # pivot lands at index p
    _quick_sort(arr, lo, p - 1)            # left of pivot
    _quick_sort(arr, p + 1, hi)            # right of pivot
```

Quick sort is the default in many language libraries (often as "introsort") because
its in-place partition has excellent cache behavior and small constants — when the
pivots are good.

## Why it works — the invariant

There are two invariants. First, the **partition invariant**, maintained as `j`
scans `lo..hi-1` with a boundary `i`:

> **Everything in `arr[lo : i]` is `<= pivot`, and everything in `arr[i : j]` is
> `> pivot`.**

`i` marks the first slot of the "greater" region. When `arr[j] <= pivot`, you swap
it into the boundary (`arr[i], arr[j] = arr[j], arr[i]`) and advance `i`, growing
the "≤" region by one. When `arr[j] > pivot`, you leave it; it joins the ">"
region. After the scan, `arr[i]` is the first element `> pivot` (or `hi` itself),
so swapping `arr[i]` with the pivot `arr[hi]` drops the pivot exactly between the
two regions. Hence:

> **After partition returns `p`: `arr[lo..p-1] <= arr[p] <= arr[p+1..hi]`, and
> `arr[p]` is in its final position.**

Second, the **recursion invariant**: `_quick_sort(arr, lo, hi)` sorts the
inclusive range `arr[lo..hi]`. By induction — the base case `lo >= hi` is a range
of size ≤ 1 (already sorted); after partition the pivot is final, and the two
recursive calls sort the strictly smaller left and right ranges. Together that
sorts the whole range. The recursion always shrinks (the pivot is excluded from
both sides via `p-1` and `p+1`), guaranteeing termination.

## Detailed walkthrough

Trace `[5, 2, 9, 1, 6, 3]` (n = 6). We show each partition fully, then recurse.

```
_quick_sort(lo=0, hi=5) on [5, 2, 9, 1, 6, 3]
PARTITION: pivot = arr[5] = 3,  i = 0
  j=0: arr[0]=5 > 3   skip                          i=0  [5, 2, 9, 1, 6, 3]
  j=1: arr[1]=2 <=3   swap a[0],a[1]; i->1          i=1  [2, 5, 9, 1, 6, 3]
  j=2: arr[2]=9 > 3   skip                          i=1  [2, 5, 9, 1, 6, 3]
  j=3: arr[3]=1 <=3   swap a[1],a[3]; i->2          i=2  [2, 1, 9, 5, 6, 3]
  j=4: arr[4]=6 > 3   skip                          i=2  [2, 1, 9, 5, 6, 3]
  place pivot: swap a[2],a[5]                        p=2  [2, 1, 3, 5, 6, 9]
  -> pivot 3 is final at index 2;  left=[2,1]  right=[5,6,9]

_quick_sort(lo=0, hi=1) on [2, 1 | ...]
PARTITION: pivot = arr[1] = 1,  i = 0
  j=0: arr[0]=2 > 1   skip                          i=0  [2, 1, ...]
  place pivot: swap a[0],a[1]                        p=0  [1, 2, ...]
  -> left = empty (lo=0,hi=-1),  right = [2] (lo=1,hi=1)  both base cases

_quick_sort(lo=3, hi=5) on [..., 5, 6, 9]
PARTITION: pivot = arr[5] = 9,  i = 3
  j=3: arr[3]=5 <=9   swap self; i->4               i=4  [..., 5, 6, 9]
  j=4: arr[4]=6 <=9   swap self; i->5               i=5  [..., 5, 6, 9]
  place pivot: swap a[5],a[5] (no-op)                p=5  [..., 5, 6, 9]
  -> left = [5,6] (lo=3,hi=4),  right = empty (lo=6,hi=5)

_quick_sort(lo=3, hi=4) on [5, 6]
PARTITION: pivot = 6 -> p=4, left=[5] base, right empty

final : [1, 2, 3, 5, 6, 9]
```

Note `j=3` in the first partition: swapping `a[1]` and `a[3]` is what makes Lomuto
**unstable** — it can jump an element over equal-valued elements between `i` and
`j`.

## Complexity, derived

The cost depends entirely on how balanced the partitions are.

- **Average / best case — balanced splits**: each partition is one O(n) scan, and a
  good pivot splits the range roughly in half. That gives the same recursion as
  merge sort:

  ```
  T(n) = 2·T(n/2) + O(n)  ->  O(n log n)
  ```

  Recursion depth ≈ log₂ n, n work per level → **O(n log n)** time.

- **Worst case — maximally unbalanced splits → O(n²).** This happens when the
  pivot is always the smallest or largest element, so one side is empty and the
  other has `n-1` elements:

  ```
  T(n) = T(n-1) + O(n)  =  n + (n-1) + ... + 1  =  n(n-1)/2  ->  O(n²)
  ```

  **Which input triggers it here?** Because this implementation always picks the
  **last element** as pivot, an **already-sorted** (or reverse-sorted) input is
  the pathological case. On `[1,2,3,4,5]`, the pivot `5` is the max, partition
  leaves `[1,2,3,4]` on the left and nothing on the right, and this repeats — a
  chain of `n` partitions, each O(n). The random tests will pass, but a sorted
  input of size 1000+ could blow the stack or crawl.

- **Space:** **O(log n)** for the recursion stack on average (depth = tree
  height), but **O(n)** in the worst case — the degenerate chain recurses `n`
  deep, which can raise `RecursionError` in Python. There is no auxiliary array
  (partition is in place), so this is the recursion stack only.

This is the core trade-off vs merge sort: quick sort wins on space and typical
speed but loses the worst-case guarantee and stability.

## Edge cases in detail

Mapped to `tests/test_quick_sort.py`:

- **Empty `[]`** (`test_edge_cases`): `quick_sort` calls `_quick_sort(arr, 0, -1)`;
  `lo >= hi` is immediately true → returns. (Note `len(arr) - 1 = -1`, handled by
  the base case.)
- **Single `[1]`**: `_quick_sort(arr, 0, 0)`, `lo >= hi` true → returns.
- **`[3, 2, 1]`**: reverse-sorted small case; exercises the unbalanced path.
- **All duplicates `[4, 4, 4, 4]`** (`test_duplicates`): every element `<= pivot`,
  so each partition puts the pivot at the far right and recurses on the rest. The
  **`<=` comparison is essential** — with `<` the equal elements would be misplaced
  and the result corrupted. This test exists specifically to catch the `<` bug.
- **In-place / returns `None`** (`test_sorts_in_place`): `assert result is None`.
  Mutate `arr`; the public `quick_sort` must not return a value.
- **Randomized vs `sorted()`** (`test_random_matches_builtin`): 50 random lists,
  sizes 0–40, compared to `sorted()`.

## Variations & trade-offs

- **Pivot choice is everything.** To dodge the O(n²) sorted-input case:
  - **Random pivot**: pick a random index in `lo..hi` and swap it to `hi` before
    partitioning. No specific input is reliably bad; expected O(n log n).
  - **Median-of-three**: take the median of `arr[lo]`, `arr[mid]`, `arr[hi]` as
    the pivot. Cheap, and makes already-sorted input a *good* case instead of the
    worst.
- **Hoare vs Lomuto partition.** This repo uses **Lomuto** (single forward scan,
  one boundary `i`, pivot at the end — simple to write, returns the pivot's final
  index). **Hoare** uses two pointers converging from both ends; it does ~3× fewer
  swaps and handles duplicates better, but its returned index is a *split point*,
  not the pivot's final slot, so the recursion bounds differ (`lo..p` and
  `p+1..hi`). Lomuto is easier to get right; Hoare is faster.
- **Three-way partition (Dutch national flag)**: split into `< pivot`, `= pivot`,
  `> pivot`. On inputs with many duplicates this turns the `[4,4,4,4]`-style worst
  case into O(n).
- **Introsort** (what C++ `std::sort` uses): start with quick sort, but if the
  recursion depth exceeds ~2·log n (signaling a bad-pivot streak), switch to heap
  sort to *guarantee* O(n log n). Also falls back to insertion sort on tiny ranges.
- **Why Timsort (Python's `sorted`) is the default instead**: Python needs a
  *stable* sort with a guaranteed O(n log n) worst case; Lomuto quick sort is
  neither stable nor worst-case-bounded. Timsort gives both, plus O(n) on
  already-ordered data.

## Connections

- [merge_sort.deep.md](merge_sort.deep.md): the stable, O(n log n)-guaranteed,
  O(n)-space counterpart. Quick sort trades those guarantees for in-place sorting
  and better constants.
- [insertion_sort.deep.md](insertion_sort.deep.md): real quick sort
  implementations switch to insertion sort on small subranges.
- [bubble_sort.deep.md](bubble_sort.deep.md): shares quick sort's O(n²) worst case
  but has no good average case.
- [../search/binary_search.md](../search/binary_search.md): binary search needs
  sorted data; quick sort is a common in-place way to produce it when stability
  is not required.

## Self-check

1. State the partition invariant in terms of `i` and `j`. What does `i` point to
   when the scan finishes?
2. After partition returns `p`, what is guaranteed about `arr[p]`? Why don't the
   recursive calls include index `p`?
3. Exactly which input makes *this* implementation hit O(n²), and why does the
   last-element pivot cause it?
4. Why must the comparison be `<=` and not `<`? Which test guards this?
5. Why is quick sort's space O(log n) average but O(n) worst, while merge sort's is
   always O(n)?
6. Name two pivot strategies that avoid the sorted-input worst case, and one way
   to *guarantee* O(n log n).

## Deep dive: common bugs

- **Returning a list from the in-place sort.** `quick_sort` must mutate `arr` and
  return `None`; `return arr` fails `assert result is None`.
- **Off-by-one in the partition loop.** The scan is `for j in range(lo, hi)` —
  it must *exclude* `hi` (the pivot). Including `hi` compares the pivot to itself
  and corrupts the boundary; stopping at `hi-1` but forgetting the final
  `swap(arr[i], arr[hi])` leaves the pivot stranded.
- **Wrong recursion bounds → infinite recursion.** You must recurse on
  `lo..p-1` and `p+1..hi`. Using `lo..p` (including the pivot) means a range can
  fail to shrink — e.g. when `p == hi`, the right call `_quick_sort(arr, p, hi)`
  recurses on the same range forever → `RecursionError`.
- **Missing the `lo >= hi` base case.** Without it, ranges of size 0 or 1 keep
  recursing (and `_partition` may index out of range), overflowing the stack.
- **`<` instead of `<=`.** Equal elements get misclassified; `[4,4,4,4]` breaks.
  Always partition with `arr[j] <= pivot`.
- **Forgetting Lomuto is unstable.** Not a correctness bug for these tests (they
  compare to `sorted()` on plain ints), but if you ever sort records by a key,
  equal keys may be reordered. Use merge sort / Timsort when stability matters.
- **Stack overflow on adversarial input.** Even correct code can `RecursionError`
  on a large sorted list because of the O(n)-deep recursion. Recursing into the
  *smaller* side first (and looping on the larger) caps stack depth at O(log n);
  a random/median pivot avoids the trigger entirely.
