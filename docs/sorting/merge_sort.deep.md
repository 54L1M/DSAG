# Merge Sort — In Depth

> In-depth companion · sorting · stub: `src/topics/sorting/merge_sort.py` · test: `tests/test_merge_sort.py`
>
> New here? Read the [quick version](merge_sort.md) first.

## The mental model

Merge sort is the textbook example of **divide and conquer**. Split the problem in
half, solve each half the same way, then combine the two solutions. The magic is
all in the *combine* step: merging two lists that are *already sorted* into one
sorted list is easy — you just repeatedly take whichever front element is smaller.

Concretely: a list of 0 or 1 elements is already sorted, so it is its own answer
(the base case). Anything longer gets split at the middle, each half is sorted
recursively, and the two sorted halves are merged. Because the recursion always
bottoms out at trivially-sorted singletons and the merge always produces sorted
output from sorted inputs, the whole thing is sorted.

Unlike bubble/insertion/quick sort in this repo, **merge sort here returns a new
list** and leaves the input untouched. The reference even copies in the base case
(`return list(arr)`) so callers never accidentally share a list with the result.

## Why it works — the invariant

The structural invariant is about the **merge** step:

> **`_merge(left, right)` returns a sorted list containing exactly the elements of
> `left` and `right`, *provided both inputs are already sorted*.**

Why merge produces sorted output: maintain two cursors `i` (into `left`) and `j`
(into `right`). At each step you append `min(left[i], right[j])` and advance that
cursor. The appended value is `<=` everything still unconsumed in *both* lists
(since both are sorted and you took the smaller front), so the output stays in
nondecreasing order. When one list empties, the other's remaining tail is already
sorted and `>=` everything appended so far, so you can `extend` it wholesale.

Then the recursion invariant: `merge_sort(arr)` returns a sorted permutation of
`arr`. By induction — the base case (length ≤ 1) is trivially sorted; the
recursive calls return sorted halves by the inductive hypothesis; `_merge`
combines two sorted halves into a sorted whole. Therefore the top-level call
returns the fully sorted list.

## Detailed walkthrough

Trace `[5, 2, 9, 1, 6, 3]` (n = 6). The split phase recurses down; the merge phase
combines back up.

```
SPLIT (mid = len//2 each time)

merge_sort([5, 2, 9, 1, 6, 3])         mid=3
  left  = merge_sort([5, 2, 9])        mid=1
            left  = merge_sort([5])    -> [5]   (base, copied)
            right = merge_sort([2, 9]) mid=1
                      [2] and [9]      -> merge -> [2, 9]
            merge([5], [2, 9])
  right = merge_sort([1, 6, 3])        mid=1
            left  = merge_sort([1])    -> [1]
            right = merge_sort([6, 3]) mid=1
                      [6] and [3]      -> merge -> [3, 6]
            merge([1], [3, 6])

MERGE (combine sorted runs)

merge([5], [2, 9]):
  cmp 5 vs 2 -> take 2     out=[2]
  cmp 5 vs 9 -> take 5     out=[2, 5]
  right tail -> extend 9   out=[2, 5, 9]

merge([1], [3, 6]):
  cmp 1 vs 3 -> take 1     out=[1]
  left empty -> extend [3,6] out=[1, 3, 6]

merge([2, 5, 9], [1, 3, 6]):
  cmp 2 vs 1 -> take 1     out=[1]
  cmp 2 vs 3 -> take 2     out=[1, 2]
  cmp 5 vs 3 -> take 3     out=[1, 2, 3]
  cmp 5 vs 6 -> take 5     out=[1, 2, 3, 5]
  cmp 9 vs 6 -> take 6     out=[1, 2, 3, 5, 6]
  left tail -> extend 9    out=[1, 2, 3, 5, 6, 9]

final : [1, 2, 3, 5, 6, 9]
```

Each `merge` call does a single linear pass over its two inputs. The original
list is never mutated — every level allocates fresh lists.

## Complexity, derived

Let `T(n)` be the work to sort `n` elements. We split into two halves and merge in
linear time:

```
T(n) = 2 · T(n/2) + O(n)
T(1) = O(1)
```

Unfold it as a **recursion tree**:

```
level 0:            n                       work n         (1 node of size n)
level 1:        n/2     n/2                 work n         (2 nodes of size n/2)
level 2:    n/4  n/4  n/4  n/4              work n         (4 nodes of size n/4)
  ...
level k:  ........ n/2^k ........           work n
  ...
leaves:   1  1  1  ... (n of them)          work n
```

- Each **level** does O(n) total merge work (the sizes at a level sum to n).
- The tree has **log₂ n + 1 levels** because you halve until you reach size 1.
- Total work = (work per level) × (number of levels) = **O(n log n)**.

This holds for best, average, *and* worst case — merge sort does the same amount
of work regardless of input order. That guaranteed O(n log n) is its headline
feature.

- **Space:** **O(n)**. Each `_merge` allocates a new list, and the slices
  `arr[:mid]` / `arr[mid:]` copy too. The dominant cost is O(n) auxiliary memory
  (plus O(log n) recursion stack). This is the price for not sorting in place —
  the opposite trade-off from quicksort.

## Edge cases in detail

Mapped to `tests/test_merge_sort.py`:

- **Empty `[]`** (`test_edge_cases`): `len(arr) <= 1` hits the base case and
  returns `list([])` → a new `[]`.
- **Single `[1]`**: base case, returns a *copy* `[1]`. (Copying matters — see
  bugs below.)
- **Two elements `[2, 1]`**: splits into `[2]` and `[1]`, merges to `[1, 2]`.
- **Returns a new sorted list, not `None`** (`test_returns_new_sorted_list`):
  `result = m.merge_sort(arr); assert result == [...]`. The contract is the
  opposite of the in-place sorts — you must *return* the answer. (The original
  `arr` is also left unmodified.)
- **Duplicates**: the random test produces many; `<=` in the merge comparison
  keeps equal elements in their original relative order — **stable**.
- **Randomized vs `sorted()`** (`test_random_matches_builtin`): 50 random lists,
  sizes 0–40, compared to `sorted()`.

## Variations & trade-offs

- **Bottom-up (iterative) merge sort**: skip recursion; merge runs of size 1, then
  2, 4, 8… with a loop. Same O(n log n), no recursion stack.
- **In-place / linked-list merge sort**: merging two linked lists needs only
  pointer rewiring — O(1) extra space — which is why merge sort is the natural
  choice for sorting linked lists. In-place array merging exists but is fiddly and
  slower.
- **External sort**: when data does not fit in RAM, merge sort streams sorted runs
  from disk and merges them — the standard approach for huge datasets.
- **Why Timsort (Python's `sorted`/`list.sort`) wins**: Timsort *is* an adaptive
  merge sort. It finds natural ascending/descending runs in the data, extends
  short ones with insertion sort, and merges runs with galloping optimizations. It
  keeps merge sort's stability and O(n log n) worst case while hitting O(n) on
  already-ordered input — something plain merge sort cannot do.

## Connections

- [quick_sort.deep.md](quick_sort.deep.md): the direct rival. Quick sort sorts in
  place (O(log n) space) and is often faster on cache, but risks O(n²) and is not
  stable. Merge sort guarantees O(n log n) and stability at O(n) space.
- [insertion_sort.deep.md](insertion_sort.deep.md): merge sort's small-array
  partner inside Timsort; also stable.
- [bubble_sort.deep.md](bubble_sort.deep.md): the O(n²) baseline merge sort
  decisively beats at scale.
- [../search/binary_search.md](../search/binary_search.md): binary search needs
  sorted input — merge sort is a stable way to produce it.

## Self-check

1. Why must both inputs to `_merge` already be sorted for it to work?
2. Why does this implementation return `list(arr)` in the base case instead of
   `arr`?
3. Derive the number of levels in the recursion tree and the work per level. How
   does that give O(n log n)?
4. Why is merge sort's space O(n) while quick sort's is O(log n)?
5. Which comparison (`<` vs `<=`) in the merge preserves stability, and why?
6. Merge sort is O(n log n) in *all* cases. Name a downside that quick sort avoids.

## Deep dive: common bugs

- **Returning `None` or sorting in place.** This contract returns a *new* list. A
  `None` return (or mutating `arr` and returning nothing) fails
  `assert result == [...]`.
- **Not copying in the base case (aliasing).** `return arr` for length ≤ 1 hands
  back a reference to the caller's list. If anything later mutates the result, the
  original mutates too — a spooky action-at-a-distance bug. `return list(arr)`
  breaks the alias. (For length-1 inputs the result *is* the input list if you
  forget this.)
- **Forgetting to drain the tail.** After the `while i < len(left) and j <
  len(right)` loop, exactly one list still has elements. You must
  `merged.extend(left[i:])` *and* `merged.extend(right[j:])`. Dropping either
  loses elements; the random test will catch the missing values.
- **A bad split.** `arr[:mid]` paired with `arr[mid+1:]` drops the element at
  `mid`. Both halves must together cover the whole list: `arr[:mid]` and
  `arr[mid:]`.
- **Splitting without progress.** If a split can produce a piece the same size as
  the input (e.g. an off-by-one that never shrinks one branch), the recursion
  never reaches the base case → infinite recursion / `RecursionError`. Halving at
  `len(arr) // 2` guarantees both pieces are strictly smaller for `n >= 2`.
- **Using `<` instead of `<=` in the merge.** Still sorts correctly but is no
  longer stable.
