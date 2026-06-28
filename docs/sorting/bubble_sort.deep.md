# Bubble Sort — In Depth

> In-depth companion · sorting · stub: `src/topics/sorting/bubble_sort.py` · test: `tests/test_bubble_sort.py`
>
> New here? Read the [quick version](bubble_sort.md) first.

## The mental model

Picture the list as a column of water. Heavy values (big numbers) sink, light
values (small numbers) rise. On each *pass* you walk left to right, looking only
at **one adjacent pair at a time**, and swap whenever the left element is larger
than the right. The single largest value you encounter keeps getting carried
rightward with you until it lands at the very end — it "bubbles up" to the top.

The key insight that makes bubble sort more than a curiosity: after pass 1 the
largest element is guaranteed to be in its final slot. After pass 2, the two
largest are. So each pass can stop one step earlier than the last. And if a pass
makes *zero* swaps, the list is already sorted and you can quit immediately.

Bubble sort is the simplest comparison sort to reason about, which is exactly why
it is the first one most people meet. It is also one of the slowest in practice,
so you will almost never ship it — but its *invariant* is a gentle on-ramp to the
way we prove every other sort correct.

## Why it works — the invariant

The loop invariant is:

> **After pass `i` completes, the last `i` elements of the list are the `i`
> largest values, and they sit in sorted order at the tail.**

Why does one pass extend the sorted tail by exactly one? During a pass, whenever
you find `arr[j] > arr[j+1]` you swap. The effect is that the largest value seen
so far always travels with the scan: the moment the scan reaches the current
maximum, every later comparison swaps it forward again, so it is deposited at the
far right end of the *unsorted* region. That is precisely the next slot of the
sorted tail.

So the unsorted region shrinks by one each pass. After `n-1` passes the unsorted
region has length 1, which is trivially sorted, and the whole list is sorted.

The early-exit refinement adds a second, stronger fact: if during any pass no
swap happens, then **every adjacent pair was already in order**, which for a list
means the entire list is sorted. So we may stop. This is what converts the
already-sorted case from O(n²) into O(n).

## Detailed walkthrough

Trace `[5, 1, 4, 2, 8, 0]` (n = 6). The `|` marks the boundary; elements to its
right are locked in their final positions.

```
start : [5, 1, 4, 2, 8, 0]

pass i=0  (scan j = 0..4)
  j0: 5>1  swap -> [1, 5, 4, 2, 8, 0]
  j1: 5>4  swap -> [1, 4, 5, 2, 8, 0]
  j2: 5>2  swap -> [1, 4, 2, 5, 8, 0]
  j3: 5<8  keep -> [1, 4, 2, 5, 8, 0]
  j4: 8>0  swap -> [1, 4, 2, 5, 0, 8]
  result      -> [1, 4, 2, 5, 0 | 8]   swapped=True, 8 locked

pass i=1  (scan j = 0..3)
  j0: 1<4  keep
  j1: 4>2  swap -> [1, 2, 4, 5, 0 | 8]
  j2: 4<5  keep
  j3: 5>0  swap -> [1, 2, 4, 0, 5 | 8]
  result      -> [1, 2, 4, 0 | 5, 8]   swapped=True, 5 locked

pass i=2  (scan j = 0..2)
  j0: 1<2  keep
  j1: 2<4  keep
  j2: 4>0  swap -> [1, 2, 0, 4 | 5, 8]
  result      -> [1, 2, 0 | 4, 5, 8]   swapped=True, 4 locked

pass i=3  (scan j = 0..1)
  j0: 1<2  keep
  j1: 2>0  swap -> [1, 0, 2 | 4, 5, 8]
  result      -> [1, 0 | 2, 4, 5, 8]   swapped=True, 2 locked

pass i=4  (scan j = 0..0)
  j0: 1>0  swap -> [0, 1 | 2, 4, 5, 8]
  result      -> [0 | 1, 2, 4, 5, 8]   swapped=True, 1 locked

pass i=5  (scan j = empty range)
  no comparisons, swapped=False -> EARLY EXIT
final : [0, 1, 2, 4, 5, 8]
```

Notice each pass scans `range(n - 1 - i)` — one fewer comparison every time —
because the tail is already done. The early-exit flag fires on the final pass.

## Complexity, derived

The inner loop on pass `i` runs `n - 1 - i` comparisons. Summing over all passes:

```
(n-1) + (n-2) + ... + 2 + 1  =  n(n-1)/2
```

That arithmetic-series sum is `≈ n²/2`, so the comparison count is **O(n²)** in
the average and worst case. Swaps are also O(n²) in the worst case (a reversed
list swaps on nearly every comparison).

- **Worst case — reversed input** `[5,4,3,2,1]`: every pass does the maximum
  work and at least one swap, so the early-exit never triggers early. O(n²).
- **Best case — already sorted** `[1,2,3,4]`: the first pass does `n-1`
  comparisons, finds nothing to swap, sets `swapped=False`, and breaks. That is
  one linear pass: **O(n)**.
- **Space:** O(1). All work is in-place swaps; no auxiliary array.

This is the whole appeal/limitation: trivial memory, but quadratic time that
makes it unusable past a few hundred elements.

## Edge cases in detail

These map directly to `tests/test_bubble_sort.py`:

- **Empty list `[]`** (`test_empty_and_single`): `n = 0`, outer loop body never
  runs a meaningful comparison; list stays `[]`. The function still returns
  `None`.
- **Single element `[7]`**: `n = 1`, inner range is empty, nothing happens.
  Already sorted.
- **Duplicates `[5, 2, 9, 1, 5, 6]`** (`test_sorts_in_place`): the two `5`s must
  end as `[1, 2, 5, 5, 6, 9]`. Because we only swap on strict `>`, the original
  left-`5` never jumps past the right-`5` — order among equals is preserved
  (**stable**).
- **Reversed `[5, 4, 3, 2, 1]`** (`test_reversed`): the worst case; verifies the
  algorithm still terminates correctly after the maximum number of swaps.
- **In-place / returns `None`**: `result = m.bubble_sort(arr); assert result is
  None`. Mutate `arr`; do not build and return a new list.
- **Randomized vs `sorted()`** (`test_random_matches_builtin`): 50 random lists
  (sizes 0–30) are compared against Python's `sorted()`. This catches subtle
  boundary bugs a hand-picked case would miss.

## Variations & trade-offs

- **Cocktail shaker sort**: alternate the scan direction each pass (left→right,
  then right→left). Helps when a small element is stranded near the end (a
  "turtle"), but it is still O(n²).
- **Comb sort**: compare elements a large gap apart and shrink the gap over time,
  killing turtles faster. Better constants, same asymptotic ceiling.
- **In practice**: essentially never used for real workloads. Its niche is
  pedagogy and tiny/almost-sorted lists where simplicity beats speed.
- **Why Timsort (Python's `sorted`) wins**: Timsort detects existing sorted runs,
  uses insertion sort on small chunks, and merges runs — giving O(n) on
  already-ordered data and O(n log n) generally, with stability. Bubble sort's
  early exit only gives you the easy O(n) case; it has no answer for the hard one.

## Connections

- [insertion_sort.deep.md](insertion_sort.deep.md): the other "grow a sorted
  region" quadratic sort; usually faster than bubble in practice because it
  shifts instead of repeatedly swapping.
- [merge_sort.deep.md](merge_sort.deep.md) and
  [quick_sort.deep.md](quick_sort.deep.md): the O(n log n) sorts you graduate to.
- [../search/binary_search.md](../search/binary_search.md): binary search needs
  *sorted* input — sorting is the precondition that unlocks it. Sorting once at
  O(n log n) then binary-searching many times at O(log n) is a classic combo.

## Self-check

1. State the loop invariant after pass `i`. Why does each pass enlarge the sorted
   tail by exactly one element?
2. Exactly what does the `swapped` flag give you, and on which input does it pay
   off? What is the time complexity without it?
3. Why is the inner loop bound `n - 1 - i` and not `n - 1`?
4. Why does using `>` (not `>=`) in the comparison keep the sort stable?
5. On `[3, 1, 2]`, how many full passes run before the early exit fires?
6. The reversed list is the worst case — roughly how many swaps does
   `[5,4,3,2,1]` perform in total?

## Deep dive: common bugs

- **Returning the list instead of `None`.** `return arr` (or returning the result
  of a comprehension) fails `assert result is None`. Bubble sort mutates in place;
  end the function with no `return`.
- **Looping `j` over the full width every pass.** Writing `for j in range(n-1)`
  instead of `range(n-1-i)` is not *wrong* output-wise (the tail is already
  sorted so no swaps happen there), but it wastes work and, worse, if you also
  index `arr[j+1]` with `range(n)` you get an `IndexError`.
- **`>=` instead of `>`.** Swapping equal elements breaks stability and burns
  swaps. If combined with a "loop until no progress" structure that counts equal
  swaps as progress, it can loop forever.
- **Dropping the early-exit flag.** Still correct, but you lose the O(n)
  best case — the `test_already_sorted` case now does full O(n²) work.
- **Building a new list.** Appending to a fresh list and returning it both
  violates the in-place contract and the `is None` assertion.
