# Binary Search — In Depth

> In-depth companion · search · stub: `src/topics/search/binary_search.py` · test: `tests/test_binary_search.py`
>
> New here? Read the [quick version](binary_search.md) first.

## The mental model

Binary search trades a one-time cost (the data must be **sorted**) for a dramatic speedup: instead of checking elements one by one, each comparison lets you throw away *half* of what remains.

Several framings of the same idea:

- **As elimination:** "Look at the middle. The target is either there, entirely to the left, or entirely to the right. Two of those three are eliminated in one comparison."
- **As a shrinking window:** maintain a half-open range `[lo, hi)` of indices that could *still* contain the target, and keep shrinking it until you find the target or the range is empty.
- **As a decision tree:** every comparison is a node with two children (go left / go right). A balanced binary tree over `n` leaves has depth ~log₂(n) — that depth is the number of comparisons.

**Analogy.** The "guess my number from 1 to 100" game. You guess 50; I say "higher." You've just deleted 1–50 with one question. Guess 75, "lower" — deletes 76–100. Each question halves the range, so you corner any number in about 7 guesses (2⁷ = 128 ≥ 100). Binary search is that game, where "higher/lower" is the comparison `arr[mid] < target`.

**Where it shows up.**
- Python's `bisect` module (`bisect_left`, `bisect_right`) is binary search; it powers efficient "insert while keeping sorted" and range queries.
- Database **B-tree indexes** are a disk-friendly generalization of this halving idea.
- "Binary search on the answer" — a classic interview pattern where you binary-search over a *range of possible answers* (not an array) using a monotonic feasibility check (e.g. minimum capacity to ship packages in D days).
- `git bisect` finds the commit that introduced a bug by halving the commit range.

This repo's signature is `binary_search(arr: list[int], target: int) -> int`. **Precondition: `arr` is ascending-sorted.** It returns an index, or `-1`. The window convention is **half-open `[lo, hi)`** — `lo` is the first index still in play, `hi` is *one past* the last. That convention is deliberate and shapes every line below.

## Why it works — the invariant

The loop maintains a window `[lo, hi)`. The invariant is:

> **If the target is anywhere in `arr`, then its index is within `[lo, hi)`.**

Equivalently: every index *outside* `[lo, hi)` has been proven not to hold the target.

Why the invariant survives each step. We compute `mid = (lo + hi) // 2`, which (because `lo < hi`) satisfies `lo <= mid < hi`, so `mid` is always a real, in-window index — we never read out of bounds. Then, since the array is sorted:

- `arr[mid] == target` → we found it, return `mid`.
- `arr[mid] < target` → because the array is ascending, **every** index `<= mid` holds a value `<= arr[mid] < target`, so none of them can be the target. We safely set `lo = mid + 1`, excluding `mid` itself (already checked) and everything left of it.
- `arr[mid] > target` → symmetrically, every index `>= mid` is too big, so we set `hi = mid`. Note `hi = mid`, **not** `mid - 1`: because `hi` is *exclusive*, setting it to `mid` already drops `mid` from the window.

Each branch only removes indices that *cannot* hold the target, so the invariant ("if present, it's in `[lo, hi)`") is preserved.

**Termination & correctness on exit.** The window strictly shrinks every iteration (proof in the bugs section), so eventually either we return `mid`, or `lo == hi` and the loop condition `lo < hi` fails. An empty window `[lo, lo)` contains no indices; by the invariant, "if the target were present its index would be in this empty range" — a contradiction — so the target is absent and `-1` is correct.

## Detailed walkthrough

Search for `6` (absent) in `[1, 3, 5, 7, 9, 11]`. Start `lo = 0, hi = 6`.

| step | lo | hi | mid = (lo+hi)//2 | arr[mid] | compare to 6 | window update      |
|------|----|----|------------------|----------|--------------|-------------------|
| 1    | 0  | 6  | 3                | 7        | 7 > 6        | hi = mid = 3      |
| 2    | 0  | 3  | 1                | 3        | 3 < 6        | lo = mid + 1 = 2  |
| 3    | 2  | 3  | 2                | 5        | 5 < 6        | lo = mid + 1 = 3  |
| —    | 3  | 3  | —                | —        | lo == hi     | loop ends → **-1** |

Watch the window collapse: `[0,6) → [0,3) → [2,3) → [3,3)`. It is always non-empty until the final step, `mid` is always inside it, and `6` would have had to live between `5` (index 2) and `7` (index 3) — a gap that doesn't exist — so `-1` is right.

Now a *found* trace — search `9` in the same array:

| step | lo | hi | mid | arr[mid] | compare to 9 | window update     |
|------|----|----|-----|----------|--------------|-------------------|
| 1    | 0  | 6  | 3   | 7        | 7 < 9        | lo = 4            |
| 2    | 4  | 6  | 5   | 11       | 11 > 9       | hi = 5            |
| 3    | 4  | 5  | 4   | 9        | equal        | **return 4**      |

Three comparisons for six elements (`log₂ 6 ≈ 2.6`, rounded up to 3).

## Complexity, derived

Let `n` be the window size, `n = hi - lo`. Each iteration replaces the window with one of roughly half the size:

- Going right: new size is `hi - (mid + 1) = hi - mid - 1 ≈ n/2 - 1`.
- Going left: new size is `mid - lo ≈ n/2`.

So after `k` iterations the window is at most `n / 2ᵏ`. The loop stops when the window is empty (or we return early). Setting `n / 2ᵏ < 1` gives `2ᵏ > n`, i.e. `k > log₂ n`. So the number of iterations is at most `⌈log₂ n⌉ + 1`.

**Time: O(log n).** Each iteration is O(1) work (one midpoint, one comparison, one assignment). Concretely: `n = 1,000,000` needs only ~20 comparisons; doubling `n` adds just *one* more comparison. That logarithmic growth is the entire point.

**Space: O(1).** Two integers, `lo` and `hi` (plus `mid`). The iterative form uses no recursion stack. (A recursive binary search would use O(log n) stack frames instead.)

The catch: this assumes sorted input. If you must sort first, that costs O(n log n) once — only worth it if you'll search many times. For a single lookup on unsorted data, plain [linear search](linear_search.md) at O(n) wins.

## Edge cases in detail

Mapped to `tests/test_binary_search.py`:

- **`test_empty` — `binary_search([], 1) == -1`.** `lo, hi = 0, 0`, so `lo < hi` is false immediately; the body never runs and `mid` is never computed. This is *why* `hi = len(arr)` and the loop guard matter — you must **not** index `arr[mid]` before confirming the window is non-empty. No special `if not arr` guard is needed.
- **`test_single` — `[42]`.** Searching `42`: `lo=0, hi=1, mid=0, arr[0]==42` → return 0. Searching `7`: `mid=0, arr[0]=42 > 7 → hi=0`, window empties → -1. The single-element case is where off-by-one bugs that *almost* work tend to surface.
- **`test_found_various` — every element of `[1,3,5,7,9,11]` is found at its own index.** Exercises midpoints landing on each position, confirming the window math hits boundaries correctly.
- **`test_not_found` — `6`, `0`, `100` in `[1,3,5,7,9]`.** Three flavors of absent: a value *between* existing elements (6), one *below the whole range* (0, window walks all the way left), and one *above* (100, window walks all the way right). Each must collapse to an empty window and return -1.

## Variations & trade-offs

- **`bisect` module.** Prefer the standard library in real code. `bisect.bisect_left(arr, x)` returns the leftmost insertion point keeping `arr` sorted; `bisect_right` the rightmost. To test membership: `i = bisect_left(arr, x); found = i < len(arr) and arr[i] == x`. These are C-implemented and battle-tested.
- **Lower bound / upper bound.** This repo's version returns *any* matching index (whichever `mid` lands on a duplicate first). To get the *first* occurrence among duplicates, don't return on equality — on `arr[mid] >= target` set `hi = mid`, else `lo = mid + 1`, then check `arr[lo]` at the end. Upper bound is symmetric. These generalize binary search to ranges.
- **Inclusive `[lo, hi]` convention.** A valid alternative: `hi = len(arr) - 1`, loop while `lo <= hi`, update `hi = mid - 1`. It works but is a *different* contract — mixing it with the half-open updates (e.g. `hi = mid` while looping `<=`) causes infinite loops. Pick one convention and apply it consistently.
- **Binary search on the answer.** When the array is conceptual — a monotonic predicate over a numeric range — binary-search the smallest input where the predicate flips from false to true. Same halving, no literal array. ([Two crystal balls](two_crystal_balls.deep.md) searches a monotonic boolean array too, but under a *drop budget* constraint that rules binary search out — see its doc.)

## Connections

- [`linear_search.deep.md`](linear_search.deep.md) — the O(n) baseline binary search beats *once data is sorted*.
- [`../sorting/merge_sort.md`](../sorting/merge_sort.md) and [`../sorting/quick_sort.md`](../sorting/quick_sort.md) — produce the sorted input binary search requires; the sort cost (O(n log n)) is what you amortize over many searches.
- [`two_crystal_balls.deep.md`](two_crystal_balls.deep.md) — a search on a sorted *boolean* array where a resource constraint forces O(√n) instead of O(log n).
- [`../trees/dfs_on_bst.md`](../trees/dfs_on_bst.md) — a binary search tree *is* binary search made into a data structure; descending it makes the same left/right decision per node.

## Self-check

1. Why is `hi = mid` (not `mid - 1`) correct under the half-open `[lo, hi)` convention, and what breaks if you use `mid - 1`?
2. Why is `lo = mid + 1` rather than `lo = mid`? What kind of bug does `lo = mid` cause?
3. Prove the window strictly shrinks every iteration (consider both branches).
4. Why can `arr[mid]` never raise `IndexError` once the loop body runs?
5. Derive the ~log₂(n) step count from the halving relation.
6. How would you modify the function to return the *first* index of a duplicated target instead of an arbitrary one?

## Deep dive: common bugs

- **Off-by-one in the window (`hi = mid - 1`).** Under half-open `[lo, hi)`, `hi` is exclusive, so `hi = mid` already excludes `mid`. Writing `hi = mid - 1` *also* drops `mid - 1`, an element that was never checked — you can skip the target and return -1 for a value that's present.
- **`lo = mid` instead of `lo = mid + 1` → infinite loop.** When the window is size 2 (`hi - lo == 2`), `mid` rounds down to `lo`. If `arr[mid] < target` and you set `lo = mid`, then `lo` never advances, `mid` recomputes to the same value forever. Always exclude the just-checked `mid`: `lo = mid + 1`.
- **Why the window provably shrinks.** Right branch: `lo` becomes `mid + 1 > lo` (since `mid >= lo`). Left branch: `hi` becomes `mid < hi` (since `mid < hi`). Either way one endpoint moves *strictly* toward the other, so `hi - lo` decreases every iteration — guaranteeing termination. The `lo = mid` bug breaks exactly this guarantee.
- **Forgetting the empty list / indexing too early.** Computing `mid` and reading `arr[mid]` *before* the `lo < hi` guard raises `IndexError` on `[]`. The structure (guard first, then `mid`, then read) makes `test_empty` pass for free.
- **Wrong loop guard for the convention.** Half-open uses `while lo < hi`. Using `while lo <= hi` with `hi = len(arr)` reads `arr[len(arr)]` out of bounds. `<=` belongs to the inclusive `[lo, hi]` convention only.
- **Integer overflow on `mid` — a non-issue in Python.** In C/Java, `(lo + hi)` can overflow a fixed-width int for large arrays, so people write `lo + (hi - lo) // 2`. Python integers are **arbitrary precision** — they grow as needed and never overflow — so `(lo + hi) // 2` is perfectly safe here. Worth knowing the defensive form exists, but it buys nothing in Python.
- **Running on unsorted data.** The invariant's correctness depends entirely on "everything left of `mid` is smaller." On unsorted input that's false, and binary search silently returns wrong answers (no crash, just garbage). The precondition is load-bearing.
