"""Race the sorts — feel O(n^2) vs O(n log n) for yourself.

Times your four sorting implementations across growing input sizes and prints a
table of milliseconds, with Python's built-in `sorted` as a baseline. The
quadratic sorts (bubble, insertion) blow up as `n` grows; the n-log-n sorts
(merge, quick) stay close to the baseline. That gap is the whole lesson.

By default it benchmarks the **active target** (whatever `.algo-target` /
`ALGO_TARGET` points at — usually your `src/topics` work). Use `--solutions` to
race the reference implementations instead. Any sort you haven't implemented yet
is simply skipped.

Examples::

    uv run python bench.py
    uv run python bench.py --sizes 1000 5000 10000
    uv run python bench.py --solutions --repeats 5
"""

from __future__ import annotations

import argparse
import os
import random
import sys
from time import perf_counter

# Quick sort recurses; give it head room for the larger inputs.
sys.setrecursionlimit(1_000_000)

SORTS = ["bubble_sort", "insertion_sort", "merge_sort", "quick_sort"]
# These return a NEW sorted list instead of sorting in place.
RETURNS_NEW = {"merge_sort"}
DEFAULT_SIZES = [500, 1000, 2000, 4000]


def run_sort(fn, name: str, data: list[int]) -> list[int]:
    """Run one sort on a fresh copy of `data` and return the sorted result."""
    arr = list(data)
    if name in RETURNS_NEW:
        return fn(arr)
    fn(arr)
    return arr


def time_sort(fn, data: list[int], repeats: int) -> float | None:
    """Best-of-`repeats` wall time in milliseconds, or None if it errors."""
    best = None
    for _ in range(repeats):
        arr = list(data)
        try:
            start = perf_counter()
            fn(arr)  # in-place or returns-new: timing the call is all we need
            elapsed = perf_counter() - start
        except NotImplementedError:
            return None
        best = elapsed if best is None else min(best, elapsed)
    return None if best is None else best * 1000.0


def load_sorts(use_solutions: bool):
    """Return {name: callable} for every sort that imports and is implemented."""
    if use_solutions:
        os.environ["ALGO_TARGET"] = "solutions"
    # Import after possibly setting ALGO_TARGET so the harness picks it up.
    from harness import load, target_root

    funcs = {}
    for name in SORTS:
        try:
            module = load(name)
            funcs[name] = getattr(module, name)
        except (ImportError, AttributeError):
            funcs[name] = None
    return funcs, target_root()


def verify(fn, name: str, data: list[int]) -> str:
    """Classify a sort before timing it: 'ok', 'not_implemented', or 'wrong'."""
    try:
        result = run_sort(fn, name, data)
    except NotImplementedError:
        return "not_implemented"
    return "ok" if result == sorted(data) else "wrong"


def fmt(ms: float | None) -> str:
    if ms is None:
        return "    —   "
    return f"{ms:8.2f}"


def main() -> None:
    parser = argparse.ArgumentParser(description="Race the sorting exercises.")
    parser.add_argument(
        "--sizes", type=int, nargs="+", default=DEFAULT_SIZES, help="input sizes to test"
    )
    parser.add_argument("--repeats", type=int, default=3, help="timed runs per cell (best wins)")
    parser.add_argument(
        "--solutions", action="store_true", help="race the reference solutions instead of your code"
    )
    parser.add_argument("--seed", type=int, default=42, help="RNG seed for reproducible inputs")
    args = parser.parse_args()

    funcs, root = load_sorts(args.solutions)
    rng = random.Random(args.seed)

    print(f"Benchmarking target: {root}")
    print(f"sizes={args.sizes}  repeats={args.repeats}  seed={args.seed}")

    # Classify every sort up front: found+correct, not yet implemented, or buggy.
    sample = [rng.randint(-1000, 1000) for _ in range(200)]
    columns: list[str] = []
    not_implemented: list[str] = []
    for name in SORTS:
        fn = funcs.get(name)
        verdict = "not_implemented" if fn is None else verify(fn, name, sample)
        if verdict == "ok":
            columns.append(name)
        elif verdict == "not_implemented":
            not_implemented.append(name)
        else:
            print(f"⚠  {name} is INCORRECT on a sample input — fix it, then re-run.")

    if not_implemented:
        print(f"not implemented yet (skipped): {', '.join(not_implemented)}")
    if not columns:
        print("\nNothing to race — implement a sort first, or pass --solutions.")
        return
    print()

    header = f"{'n':>8} | " + " | ".join(f"{c:>10}" for c in [*columns, "sorted"])
    print(header)
    print("-" * len(header))

    for n in args.sizes:
        data = [rng.randint(-(10**6), 10**6) for _ in range(n)]
        cells = [fmt(time_sort(funcs[name], data, args.repeats)) for name in columns]
        # Baseline: Python's Timsort (C-implemented).
        cells.append(fmt(time_sort(lambda a: a.sort(), data, args.repeats)))
        print(f"{n:>8} | " + " | ".join(f"{c:>10}" for c in cells))

    print("\n(ms, lower is better. Watch the n^2 sorts pull away as n grows.)")


if __name__ == "__main__":
    main()
