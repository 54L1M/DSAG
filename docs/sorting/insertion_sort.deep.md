# Insertion Sort — In Depth

> In-depth companion · sorting · stub: `src/topics/sorting/insertion_sort.py` · test: `tests/test_insertion_sort.py`
>
> New here? Read the [quick version](insertion_sort.md) first.

## The mental model

This is how almost everyone sorts a hand of playing cards without thinking about
it. The cards in your left hand are already in order. You pick up the next card
and slide it leftward, past every card bigger than it, until it clicks into the
right spot. Repeat until there are no cards left to pick up.

In array terms: at every step there is a **sorted prefix** `arr[:i]` and an
unsorted tail. You take the first unsorted element, call it `key`, and open a gap
for it by shifting the larger prefix elements one slot to the right. Then you drop
`key` into the gap. The sorted prefix is now one longer.

Two things distinguish insertion sort from bubble sort even though both are O(n²):
it *shifts* (one write per moved element) rather than *swaps* (three writes per
move), and it stops the inner loop the instant it finds the insertion point. On
nearly-sorted data those inner loops barely run, which is why insertion sort is
genuinely fast on small or almost-ordered inputs — and why Timsort uses it as its
small-array building block.

## Why it works — the invariant

The loop invariant is:

> **At the start of each iteration `i`, the slice `arr[:i]` is sorted (a
> permutation of the original first `i` elements, in ascending order).**

- **Establishment:** before `i = 1`, the prefix `arr[:1]` is a single element,
  which is sorted by definition.
- **Maintenance:** iteration `i` removes `key = arr[i]` and shifts every prefix
  element greater than `key` rightward, then inserts `key` at the gap. Everything
  left of the gap is `<= key`; everything to its right (that we shifted) is
  `> key` and was already sorted among itself. So `arr[:i+1]` is now sorted.
- **Termination:** the loop ends after `i = n-1`, so `arr[:n]` — the whole list —
  is sorted.

The inner `while j >= 0 and arr[j] > key` is doing two jobs: `j >= 0` keeps you
inside the array, and `arr[j] > key` stops as soon as you reach an element that is
not larger than `key` — that is the insertion point.

## Detailed walkthrough

Trace `[5, 1, 4, 2, 8, 0]` (n = 6). `|` marks the end of the sorted prefix.
Inside each step, `_` shows the open gap as `key` slides left.

```
start : [5 | 1, 4, 2, 8, 0]                key picked from arr[i]

i=1  key=1
  j=0: arr[0]=5 > 1  shift 5 right -> [_, 5 | 4, 2, 8, 0]
  j=-1: stop, drop key -> [1, 5 | 4, 2, 8, 0]

i=2  key=4
  j=1: arr[1]=5 > 4  shift 5 -> [1, _, 5 | 2, 8, 0]
  j=0: arr[0]=1 <=4  stop, drop -> [1, 4, 5 | 2, 8, 0]

i=3  key=2
  j=2: arr[2]=5 > 2  shift 5 -> [1, 4, _, 5 | 8, 0]
  j=1: arr[1]=4 > 2  shift 4 -> [1, _, 4, 5 | 8, 0]
  j=0: arr[0]=1 <=2  stop, drop -> [1, 2, 4, 5 | 8, 0]

i=4  key=8
  j=3: arr[3]=5 <=8  stop immediately, drop in place -> [1, 2, 4, 5, 8 | 0]
       (this is the cheap "already in order" case: zero shifts)

i=5  key=0
  j=4: 8 > 0  shift -> [1, 2, 4, 5, _, 8]
  j=3: 5 > 0  shift -> [1, 2, 4, _, 5, 8]
  j=2: 4 > 0  shift -> [1, 2, _, 4, 5, 8]
  j=1: 2 > 0  shift -> [1, _, 2, 4, 5, 8]
  j=0: 1 > 0  shift -> [_, 1, 2, 4, 5, 8]
  j=-1: stop, drop -> [0, 1, 2, 4, 5, 8]

final : [0, 1, 2, 4, 5, 8]
```

Watch step `i=4`: `key=8` is already bigger than everything in the prefix, so the
inner loop does **zero** iterations. That cheap exit is the whole reason
insertion sort shines on sorted-ish data. Step `i=5` is the opposite: the new
element is the new minimum and must slide all the way to the front.

## Complexity, derived

Iteration `i` does *at most* `i` shifts (when `key` is smaller than the entire
prefix). Summing the worst case over all iterations:

```
1 + 2 + 3 + ... + (n-1)  =  n(n-1)/2  ≈ n²/2   ->  O(n²)
```

- **Worst case — reverse-sorted** `[5,4,3,2,1]`: every `key` is the new minimum
  and slides past the whole prefix. Full `n(n-1)/2` shifts. O(n²).
- **Best case — already sorted** `[1,2,3,4,5]`: each `key` is already `>=` the end
  of the prefix, so each inner `while` exits on its first test. `n-1` comparisons
  total, zero shifts: **O(n)**.
- **Nearly sorted**: if every element is at most `k` slots from its final
  position, the cost is O(n·k) — effectively linear for small `k`. This is the
  property Timsort exploits.
- **Space:** O(1) — one `key` variable, all shifting in place.

Insertion sort typically beats bubble sort by a constant factor: a *shift* is one
array write, whereas a *swap* is three. Same big-O, smaller constant.

## Edge cases in detail

Mapped to `tests/test_insertion_sort.py`:

- **Empty `[]`** (`test_edge_cases`): `range(1, 0)` is empty; the outer loop never
  runs. List stays `[]`, returns `None`.
- **Single `[1]`**: `range(1, 1)` is empty; nothing to insert. Already sorted.
- **Two elements `[2, 1]`**: one iteration, `key=1` shifts `2` right, result
  `[1, 2]`. The minimal real sort.
- **Duplicates `[5, 2, 9, 1, 5, 6]`** (`test_sorts_in_place`): expected
  `[1, 2, 5, 5, 6, 9]`. The strict `>` in the while condition means a later `5`
  stops *at* the earlier `5` rather than sliding past it — **stable**.
- **In-place / returns `None`**: `assert result is None`. Mutate `arr`; no return
  value.
- **Randomized vs `sorted()`** (`test_random_matches_builtin`): 50 random lists,
  sizes 0–30, checked against `sorted()`.

## Variations & trade-offs

- **Binary insertion sort**: use binary search to *find* the insertion point in
  O(log i) instead of scanning. Reduces comparisons to O(n log n), but you still
  *shift* O(n²) elements, so total work stays O(n²). Helps when comparisons are
  expensive (e.g. comparing long strings).
- **Gapped insertion = Shell sort**: insertion-sort elements that are a large gap
  apart, then shrink the gap. Lets elements make big jumps early, beating plain
  O(n²) in practice (around O(n^1.25)–O(n^1.5) depending on the gap sequence).
- **In practice**: the go-to for *small* arrays (roughly n ≤ 16–32) and for
  nearly-sorted data. Real library sorts (including CPython's Timsort) switch to
  insertion sort for small runs precisely because its constants are tiny there.
- **Why Timsort wins overall**: it splits the input into natural runs, insertion-
  sorts short ones, and merges them in O(n log n) — keeping insertion sort's O(n)
  behavior on ordered data while avoiding the quadratic blow-up on random data.

## Connections

- [bubble_sort.deep.md](bubble_sort.deep.md): the other quadratic "grow a sorted
  region" sort; insertion shifts where bubble swaps, so insertion is usually
  faster.
- [merge_sort.deep.md](merge_sort.deep.md): also stable, but O(n log n) and uses
  O(n) extra space; Timsort fuses merge sort with insertion sort.
- [quick_sort.deep.md](quick_sort.deep.md): faster on large random data but not
  stable and risks O(n²); often falls back to insertion sort on small subranges.
- [../search/binary_search.md](../search/binary_search.md): binary search needs
  sorted data — and binary *insertion* sort uses binary search internally.

## Self-check

1. State the invariant on `arr[:i]`. What makes it true before the first
   iteration, and why does each iteration preserve it?
2. Why does the inner loop test `j >= 0` *and* `arr[j] > key`, and why in that
   order?
3. Why is the final placement `arr[j + 1] = key` rather than `arr[j] = key`?
4. Give the input that triggers the O(n) best case and the one that triggers the
   O(n²) worst case.
5. Insertion and bubble are both O(n²). Name one concrete reason insertion sort is
   usually faster in practice.
6. On `[5, 2, 9, 1, 5, 6]`, how many shifts happen when inserting the second `5`?

## Deep dive: common bugs

- **Returning the list instead of `None`.** `return arr` fails `assert result is
  None`. Insertion sort mutates in place.
- **Off-by-one on placement.** When the `while` ends, `j` sits one slot *left* of
  the gap (either it found `arr[j] <= key`, or `j` fell to `-1`). The correct
  drop is `arr[j + 1] = key`. Writing `arr[j] = key` overwrites the wrong slot.
- **Overwriting `key` before saving it.** You must capture `key = arr[i]` *before*
  any shifting; the first shift `arr[j+1] = arr[j]` can clobber `arr[i]`.
- **Dropping the `j >= 0` guard.** Without it, when `key` is the new minimum, `j`
  goes negative and `arr[j]` wraps around to the end of the list (Python negative
  indexing) — silently comparing against the wrong element and corrupting the
  sort.
- **Using `>=` instead of `>`.** Equal elements shift past each other, breaking
  stability (and doing pointless extra writes).
