# Linear Search — In Depth

> In-depth companion · search · stub: `src/topics/search/linear_search.py` · test: `tests/test_linear_search.py`
>
> New here? Read the [quick version](linear_search.md) first.

## The mental model

Linear search is the most honest algorithm there is: it makes **no assumptions** and does **no preparation**. You have a pile of things and a target; you look at each thing in turn until one matches, then you stop.

Three ways to say the same idea:

- **As a loop:** "for each element, is this it? if so, return where I am; if I run out, say -1."
- **As a promise:** "I will return the index of the *first* element equal to the target, scanning left to right, or -1 if no element equals it."
- **As a filter that short-circuits:** it is `next((i for i, v in enumerate(arr) if v == target), -1)` — the first index whose value matches, defaulting to -1.

**Analogy.** You walk into a parking garage and want to find *your* car. You don't have a map, the cars aren't sorted by color or plate, so you just drive lane by lane reading plates until you spot yours. That steady, order-agnostic scan is linear search. The moment you spot it you stop — you don't keep checking the rest of the garage.

**Where it shows up in real systems.**
- `list.index(x)` and the `in` operator on a Python list are linear scans under the hood.
- `grep` reading a log file line by line is linear search over lines.
- Any "find the first record matching a predicate" over an **unindexed** collection — a database doing a full table scan because no index exists is doing exactly this.
- In interviews it is the baseline you're expected to *beat* (with sorting + binary search, or a hash set) — but also the correct answer when data is small, unsorted, or searched only once.

The signature is `linear_search(arr: list[int], target: int) -> int`. It returns an **index** (a position), never a boolean and never the value. The "not found" sentinel is exactly `-1`.

## Why it works — the invariant

The loop walks an index `i` from `0` upward. The invariant — the thing that is true every time we are about to test position `i` — is:

> **None of the elements `arr[0 .. i-1]` equals the target.**

Why this guarantees correctness:

- **Establishment.** Before the first iteration, `i = 0`, so the range `arr[0 .. -1]` is empty. "None of nothing matches" is vacuously true.
- **Maintenance.** At step `i` we test `arr[i]`. If it matches, we return `i` — and because the invariant said nothing before `i` matched, this `i` is provably the *first* match. If it does not match, then now nothing in `arr[0 .. i]` matches, so the invariant holds for `i+1`.
- **Termination.** The loop ends either by returning (we found the first match) or by exhausting all `n` indices. If it exhausts them, the invariant at the end says nothing in `arr[0 .. n-1]` — i.e. the whole list — matches, so `-1` is correct.

That "first match" property falls directly out of scanning left to right and returning *immediately*. It is the part people break when they keep looping after a match.

## Detailed walkthrough

Search for `7` in `[9, 1, 7, 3, 7]` (note: two 7s — we must return the *first*, index 2).

| step | i | arr[i] | invariant before this step ("none of arr[0..i-1] == 7") | arr[i] == 7? | action       |
|------|---|--------|----------------------------------------------------------|--------------|--------------|
| 1    | 0 | 9      | arr[0..-1] empty — holds                                 | no           | i → 1        |
| 2    | 1 | 1      | {9} has no 7 — holds                                     | no           | i → 2        |
| 3    | 2 | 7      | {9,1} has no 7 — holds                                   | yes          | **return 2** |

We never even look at indices 3 and 4. The second `7` at index 4 is irrelevant because we already returned.

Now a *not-found* trace — search `99` in `[1, 2, 3]`:

| step | i | arr[i] | arr[i] == 99? | action |
|------|---|--------|---------------|--------|
| 1    | 0 | 1      | no            | i → 1  |
| 2    | 1 | 2      | no            | i → 2  |
| 3    | 2 | 3      | no            | i → 3  |
| —    | 3 | —      | loop ends (i == n) | **return -1** |

Every element was touched; the invariant at the end covers the whole list, so `-1` is justified.

## Complexity, derived

Let `n = len(arr)`.

- **Best case:** target at index 0 → 1 comparison → O(1).
- **Worst case:** target at the last index, or absent → `n` comparisons → O(n).
- **Average case (target present, uniformly random position):** the expected number of comparisons is `(1 + 2 + ... + n) / n = (n+1)/2`, which is still O(n).

So the time is **O(n)**: every comparison does O(1) work, and you do at most `n` of them. There is no way to do better *without extra structure* — if the data is unsorted and unindexed, any correct algorithm must in the worst case inspect every element, because the target could be hiding in the one slot it didn't check. That lower bound is why linear search is optimal for unstructured search.

**Space: O(1).** The only state is the loop index (and in the `enumerate` form, the current value). Nothing scales with `n`.

## Edge cases in detail

These map directly to `tests/test_linear_search.py`:

- **`test_empty` — `linear_search([], 1) == -1`.** The loop body never runs (`enumerate([])` yields nothing), so we fall straight to `return -1`. A clean loop handles this for free; you do **not** need a special `if not arr` guard.
- **`test_first_and_last` — `[4, 2, 8]` finds `4` at 0 and `8` at 2.** Confirms both boundaries: the very first element (no iterations skipped) and the very last (full scan needed).
- **`test_not_found` — `99` in `[1, 2, 3]` → -1.** Full traversal, no match, correct sentinel.
- **`test_unsorted_ok` — `7` in `[9, 1, 7, 3]` → 2.** This is the test that punishes anyone who "optimizes" with sorted-list assumptions. Linear search must work on arbitrary order.
- **Duplicates (implied by the contract):** if the target appears twice, the first index wins. Returning *immediately* on match is what enforces this.

## Variations & trade-offs

- **Return the value or a boolean instead of an index.** Different contract; here the tests demand an index. Returning `i` is strictly more informative — the caller can derive presence from `i != -1`.
- **Find the *last* match:** don't return early; track `last = i` on each match and return it at the end. That forces a full O(n) scan every time (you can't short-circuit).
- **Find *all* matches:** collect into a list, `[i for i, v in enumerate(arr) if v == target]`. O(n) time, O(k) space for k matches.
- **Sentinel search (micro-optimization):** append the target to the end so the loop is guaranteed to find it, removing the per-step bounds check. Faster in low-level languages; pointless in Python where the bounds check is internal.
- **When to upgrade:** if you search the same data many times, pay an upfront cost once to make later searches cheap — sort it and use [binary search](binary_search.md) for O(log n) lookups, or build a `set`/`dict` for O(1) average lookups. Linear search wins only when data is tiny, searched rarely, or genuinely unsorted-and-one-shot.

| approach        | preprocessing | per-query | works on unsorted? |
|-----------------|---------------|-----------|--------------------|
| linear search   | none          | O(n)      | yes                |
| binary search   | O(n log n) sort | O(log n) | needs sorted       |
| hash set/dict   | O(n) build    | O(1) avg  | yes                |

## Connections

- [`binary_search.deep.md`](binary_search.deep.md) — the payoff of sorting: O(log n) instead of O(n), but only on sorted input.
- [`two_crystal_balls.deep.md`](two_crystal_balls.deep.md) — uses a *linear walk* as its second phase; the inner scan there is exactly this algorithm over a small window.
- [`../hashing/map.md`](../hashing/map.md) — the O(1)-average alternative when you can afford to build an index.
- [`../sorting/merge_sort.md`](../sorting/merge_sort.md) — one way to produce the sorted input that unlocks binary search.

## Self-check

1. Why does the empty-list case need no special-casing in a well-written loop?
2. The contract says "first match." Which single line of code enforces *first* rather than *last*?
3. What is the exact expected number of comparisons when the target is present at a uniformly random position?
4. Why can't any correct search on unsorted, unindexed data beat O(n) in the worst case?
5. If you needed to find the last occurrence instead of the first, what changes — and what do you lose?
6. State the loop invariant in your own words and explain why it implies `-1` is correct at the end.

## Deep dive: common bugs

- **Returning a boolean.** `return True`/`False` violates the index contract. Tests compare against `2`, `0`, `-1`, etc.
- **Wrong sentinel.** `return None` or `return 0` for "not found." `0` is especially nasty — it is a *valid index*, so it silently lies about a match at the front. The contract is exactly `-1`.
- **Returning the last match.** Continuing the loop after a hit (or comparing from the right) returns the wrong index when duplicates exist. Return on first match.
- **Adding a sorted-data early exit.** Logic like `if arr[i] > target: return -1` assumes ascending order and breaks on the `test_unsorted_ok` case. Linear search must stay order-agnostic.
- **Off-by-one when hand-rolling indices.** `for i in range(len(arr))` is correct; `range(len(arr) - 1)` silently skips the last element and fails `test_first_and_last`'s `8`-at-index-2. Prefer `enumerate(arr)` to sidestep this entirely.
- **Indexing before checking bounds.** Not an issue with a `for` loop, but if you write a manual `while i < len(arr)` make sure the bounds test comes *before* `arr[i]`, or an empty/exhausted list raises `IndexError`.
