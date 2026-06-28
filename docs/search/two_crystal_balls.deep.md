# Two Crystal Balls — In Depth

> In-depth companion · search · stub: `src/topics/search/two_crystal_balls.py` · test: `tests/test_two_crystal_balls.py`
>
> New here? Read the [quick version](two_crystal_balls.md) first.

## The mental model

You have a building and **two identical crystal balls**. There is some lowest floor from which a dropped ball breaks; from every floor above it breaks too, and from every floor below it survives. You want that lowest breaking floor. The constraint that makes this interesting: you only get **two balls**. Break both and you're done — no more drops allowed.

In code, the building is a boolean list `breaks` shaped `False ... False, True ... True` (a single transition from "survives" to "breaks"). You return the **index of the first `True`**, or `-1` if there is none.

Several ways to see it:

- **As a constrained search:** find the boundary in a sorted boolean array, but you may only "drop" (test a `True` and learn the window) a *very limited* number of times before you must switch to careful, one-at-a-time scanning.
- **As two phases:** a coarse phase (big jumps of `√n` to find *which region* contains the boundary) and a fine phase (a linear walk of that ~`√n`-wide region).
- **As balancing two costs:** if jumps are size `j`, the coarse phase costs ~`n/j` and the fine phase costs ~`j`. You minimize `n/j + j` by choosing `j = √n`, which is the whole reason `√n` appears.

**Analogy.** Imagine checking which page of a long book has a coffee stain that bleeds through to all later pages. With *unlimited* peeks you'd binary-search. But suppose tearing a checked page costs you, and you can only afford two "exploratory tears." So you flip ahead in big chunks (every 30 pages) to bracket the stain, then once you've overshot you flip back and read one page at a time through that 30-page band. Coarse, then fine.

**Where it shows up.**
- Classic interview problem ("egg drop" / "two eggs, 100 floors") — the canonical test of *adapting an algorithm to a resource budget*.
- The `√n` decomposition reappears in **sqrt decomposition** data structures (range queries split an array into `√n` blocks) and in **rsync's** rolling-block scheme.
- Any "find a threshold but expensive/destructive tests" scenario: hardware stress tests that damage the unit, A/B ramp where each step has a cost, etc.

Signature: `two_crystal_balls(breaks: list[bool]) -> int`. Returns the first `True` index, or `-1`.

## Why it works — the invariant

The algorithm has two loops, each with its own invariant.

**Phase 1 — the jump loop.** It checks `breaks[jump]`, `breaks[2*jump]`, … advancing `i` by `jump` each time, stopping at the first jump point that is `True` (or when `i` runs past the end). The invariant:

> **Every jump point we have already passed was `False` — so the first `True`, if it exists, is at an index `> i - jump`.**

Because the array is monotonic (`False`s then `True`s), a `False` at index `p` proves *everything at or below `p` is `False`*. So when we finally see `breaks[i] == True` (or fall off the end), the boundary cannot be at or before the *previous* jump point `i - jump`. It must lie in the half-open window `(i - jump, i]` — a band of at most `jump ≈ √n` indices.

**Phase 2 — the linear walk.** We step back to `i - jump` and scan forward up to `jump + 1` positions. The invariant here is the same as plain [linear search](linear_search.md) restricted to that window:

> **The first `True` in the whole array is the first `True` we encounter while scanning this window left to right.**

Phase 1 guarantees the boundary is *inside* this window; scanning the window from its left edge and returning on the first `True` therefore returns the global first `True`. If the scan finds no `True` (the array never breaks, or we walked the final short window and it's all `False`), we return `-1`.

**Why step back exactly one jump?** The boundary sits strictly *after* the last `False` jump point and *at or before* the current `True` jump point. The last `False` jump point is `i - jump`. Starting the walk there (not at `i`) is what makes the window cover the boundary — start at `i` and you'd miss everything between the two jump points.

## Detailed walkthrough

`n = 50`, first `True` at index `42`. `jump = int(√50) = 7`.

**Phase 1 — jumps of 7:**

| i  | breaks[i] (i >= 42?) | action               |
|----|----------------------|----------------------|
| 7  | False                | i += 7 → 14          |
| 14 | False                | i += 7 → 21          |
| 21 | False                | i += 7 → 28          |
| 28 | False                | i += 7 → 35          |
| 35 | False                | i += 7 → 42          |
| 42 | **True**             | break — window is (35, 42] |

Now `i = 42`. Step back: `i -= jump` → `i = 35`. Boundary is somewhere in indices 35..42.

**Phase 2 — linear walk, up to `jump + 1 = 8` steps from i = 35:**

| iter | i  | i < n? | breaks[i] | action       |
|------|----|--------|-----------|--------------|
| 1    | 35 | yes    | False     | i → 36       |
| 2    | 36 | yes    | False     | i → 37       |
| 3    | 37 | yes    | False     | i → 38       |
| 4    | 38 | yes    | False     | i → 39       |
| 5    | 39 | yes    | False     | i → 40       |
| 6    | 40 | yes    | False     | i → 41       |
| 7    | 41 | yes    | False     | i → 42       |
| 8    | 42 | yes    | **True**  | **return 42**|

Total ball-drops: 6 (jumps) + 8 (walk) = 14 — comfortably ~2√50 ≈ 14. Compare to linear search, which would need 43 checks.

**A subtle case — the boundary is past the last jump point.** Suppose `n = 50`, first `True` at `49`, `jump = 7`. Jumps hit 7,14,21,28,35,42 (all `False`), then `i += 7 → 49 < 50`, `breaks[49] == True` → break. Step back to `i = 42`, walk forward up to 8 steps: 42..49, finding `True` at 49. The `i < n` guard inside the walk matters because the last window can extend right up to (or past) `n`.

## Complexity, derived

Let `jump = √n`.

- **Phase 1** advances by `jump` each step, covering at most `n` indices → at most `n / jump = n / √n = √n` checks.
- **Phase 2** scans at most `jump + 1 = √n + 1` indices → `√n` checks.
- **Total:** `√n + √n = 2√n` checks → **O(√n)** time. **Space: O(1)** (a couple of index variables).

**Why `√n` is the optimal jump size.** With jump size `j`, total work is `n/j` (coarse) + `j` (fine). Minimize `f(j) = n/j + j`: `f'(j) = -n/j² + 1 = 0 → j² = n → j = √n`. At that point both phases cost `√n` and they're *balanced*. Pick `j` too small and the coarse phase dominates (toward O(n)); too large and the fine phase dominates. `√n` is the sweet spot.

**Why two balls forces O(√n) instead of O(log n).** With **one** ball you can't afford to be wrong even once — if you drop from a floor and it breaks, you've used your only ball and must already know the answer. So one ball forces pure linear search from the bottom: O(n).

With **unlimited** balls you can binary-search: drop from the middle floor; if it breaks, the boundary is below (recurse on the lower half); if not, above. Each drop halves the candidates → O(log n). But binary search's *first* drop might be from a very high floor — if it breaks, you've spent a ball and learned only "boundary ≤ here," still facing a huge range with at most one ball left. That second ball can then only walk linearly, which over a half-sized range is O(n). So binary search's drop *pattern* is unsafe under a two-ball budget.

Two balls is the in-between regime. The first ball is your "expensive, coarse" probe — you can afford to lose it, but only on `√n`-sized jumps. The second ball is your "safe, fine" probe — used for the careful linear walk that *cannot* overshoot. The budget of exactly two destructive probes is precisely what makes `√n` (not `log n`, not `n`) the right granularity. More generally, with `k` balls the optimal cost is O(n^(1/k)) — two balls is the `k = 2` case, `n^(1/2) = √n`.

## Edge cases in detail

Mapped to `tests/test_two_crystal_balls.py` (the helper `_make(n, first)` builds `[i >= first for i in range(n)]`):

- **`test_empty` — `two_crystal_balls([]) == -1`.** The `if n == 0: return -1` guard handles this. Without it, `jump = max(1, int(√0)) = 1`, the jump loop never runs (`i = 1` is not `< 0`), and you'd step back and index incorrectly — the explicit guard is cleanest.
- **`test_breaks_at_zero` — first `True` at index 0.** Phase 1's first check is `breaks[jump]` (not `breaks[0]`!), which is already `True`, so it breaks immediately at `i = jump`. Step back to `i = 0`, walk forward, find `True` at 0. This is why the walk **must** start at the window's left edge — the boundary can be index 0, which the jump phase never tests directly.
- **`test_breaks_at_last` — first `True` at index `n-1`.** Exercises the `i < n` guard in the walk; the boundary sits at the very end of the final, possibly-short window.
- **`test_never_breaks` — all `False`.** Phase 1 runs off the end (`i >= n`) without breaking. Step back, walk the final window, find no `True`, fall through to `return -1`.
- **`test_many_positions` — `n in (1,2,5,16,17,64,81,99)`, every `first` in range.** The stress test. It includes perfect squares (16, 64, 81) and non-squares (5, 17, 99) and tiny `n` (1, 2). `n = 1`: `jump = max(1, 1) = 1`; the `max(1, ...)` floor is what prevents `jump = 0` (which would be an infinite loop) when `int(√n)` rounds down to 0 for very small `n`.

## Variations & trade-offs

- **Why not binary search?** It would find the boundary in O(log n) *with no ball limit*, but its drop pattern can require a probe from near the top whose break strands you with one ball over a large range. The two-ball constraint is the entire problem; binary search ignores it. (See the complexity section.)
- **Fixed jump size (e.g. constant 10).** Works correctly but isn't O(√n): coarse cost is `n/10` (linear in `n`). Only `√n` keeps both phases at O(√n). The `√n` choice is the lesson, not an implementation detail.
- **`k` balls generalization.** With `k` balls the optimal is O(n^(1/k)): make the first ball jump in chunks of n^((k-1)/k), then recurse with `k-1` balls inside the chunk. Two balls (`k = 2`) gives `n^(1/2) = √n`; three balls gives the cube root; the limit (`k → log n`) recovers binary search's O(log n).
- **Jump-then-walk vs. walk-then-jump.** Always coarse first, fine second. The fine (linear, safe) phase must come last because it's the one that cannot overshoot — it's where you spend your irreplaceable second ball.

## Connections

- [`linear_search.deep.md`](linear_search.deep.md) — phase 2 is literally a linear search over the `√n`-wide window.
- [`binary_search.deep.md`](binary_search.deep.md) — the O(log n) search you'd use *without* the two-ball budget; contrast its drop pattern with why it's unsafe here.
- [`../sorting/merge_sort.md`](../sorting/merge_sort.md) — like binary search, this relies on a sorted (here, monotonic boolean) input; the single `False→True` transition is the precondition.

## Self-check

1. Why does phase 1 start checking at `breaks[jump]` rather than `breaks[0]`, and how does the algorithm still catch a boundary at index 0?
2. Derive `j = √n` by minimizing the total cost `n/j + j`.
3. Explain precisely why a two-ball budget rules out binary search but a single ball forces O(n).
4. Why must you step back exactly `jump` before the linear walk — what's missed if you start the walk at the current `i`?
5. What goes wrong if `jump` could be `0`, and which line prevents it?
6. With three crystal balls, what would the optimal time complexity be, and why?

## Deep dive: common bugs

- **Forgetting to step back before the walk.** The boundary lives *between* the last two jump points, not at the `True` jump point. Skipping `i -= jump` makes the walk start past the boundary and miss it. The walk must begin at the last *known-`False`* jump point.
- **Off-by-one in the walk length.** The window spans `(i - jump, i]`, up to `jump + 1` indices once you start at `i - jump` inclusive. Walking only `jump` steps can drop the last index; the reference loops `range(jump + 1)`.
- **Walking off the end (`IndexError`).** The final window may extend past `n` (e.g. boundary near the end, or the last jump landed near `n`). Every access in the walk needs an `i < n` guard. `test_breaks_at_last` and the non-square `n` values in `test_many_positions` catch this.
- **`jump = 0` → infinite loop.** For small `n`, `int(math.sqrt(n))` can be 0 (it isn't for `n >= 1` since `√1 = 1`, but the defensive `max(1, ...)` documents intent and is robust). A zero jump means `i += 0` forever. `jump = max(1, int(math.sqrt(n)))` prevents it.
- **Forgetting the empty list.** `n == 0` should short-circuit to `-1`; otherwise the step-back/walk logic operates on a nonexistent array. `test_empty` enforces this.
- **Forgetting the "never breaks" case.** All-`False` means phase 1 exhausts the array and phase 2 finds nothing — the function must fall through to `return -1`, not return a stale index. `test_never_breaks` checks it.
- **Using a constant jump and thinking it's O(√n).** A fixed jump (say 10) is O(n) in the coarse phase. The complexity claim only holds when the jump scales as `√n`.
