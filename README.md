# DSAG — DSA Gym (Python)

A study-and-practice environment for data structures & algorithms, inspired by
ThePrimeagen's [DSA course](https://frontendmasters.com/courses/algorithms/) but
built from scratch for Python and for *learning by doing*.

The loop for each topic:

1. **Study** the explainer in `docs/` (each topic has a concise doc plus an
   in-depth `*.deep.md` companion for when you want the full reasoning).
2. **Implement** the empty stub in `src/topics/<category>/`.
3. **Verify** with `pytest` — the tests run against *your* code.
4. **Check** against the worked answer in `solutions/` only if you're stuck.
5. **Drill** later: `python drill.py` gives you fresh blank stubs to redo from
   scratch. Repetition is how this stuff moves into muscle memory.

## Setup

```bash
uv sync          # creates .venv and installs pytest + ruff
```

### Makefile shortcuts

If you have `make`, it wraps the common commands — run `make` to see them all:

```bash
make setup                    # uv sync
make test k=binary_search     # run one topic's tests
make test                     # run everything
make test-solutions           # sanity-check: solutions are all green
make lint        / make fmt   # ruff check / ruff format
make drill       / make topics  # new drill day / back to study workspace
make bench ARGS="--solutions" # race the sorts
```

## Daily workflow

```bash
# 1. Pick a topic, read its doc, e.g. docs/search/binary_search.md
# 2. Open the matching stub, e.g. src/topics/search/binary_search.py
# 3. Implement it, then run just that test:
uv run pytest -k binary_search

# Run everything:
uv run pytest

# Lint / format your code (same rules apply to your solutions):
uv run ruff check
uv run ruff format
```

When a test is green, you're done. If you want to compare approaches, peek at
`solutions/binary_search.py`.

## Drilling for repetition

```bash
uv run python drill.py            # fresh blank stubs in src/days/day1, target -> day1
uv run pytest                     # now tests your day1 work
uv run python drill.py            # tomorrow: day2, all blank again
uv run python drill.py --topics   # go back to the src/topics study workspace
uv run python drill.py --show     # which target is active right now?
```

`src/days/` is gitignored scratch space — your "first pass" work in
`src/topics/` is never touched.

## Race the sorts

Once you've written some sorts, *feel* the complexity difference:

```bash
uv run python bench.py                       # races your sorts (active target)
uv run python bench.py --solutions           # races the reference solutions
uv run python bench.py --sizes 1000 5000 10000
```

It prints milliseconds per sort across growing input sizes, with Python's
built-in `sorted` as a baseline. The O(n²) sorts (bubble, insertion) pull away
hard as `n` grows while the O(n log n) sorts (merge, quick) stay near the
baseline — that gap *is* the lesson. Unimplemented or incorrect sorts are
skipped (with a note).

## How the test target works

Tests never hardcode a path; they call `harness.load("binary_search")`, which
imports `binary_search.py` from the **active target**. The active target is, in
order of precedence:

1. the `ALGO_TARGET` environment variable, or
2. the contents of `.algo-target` (managed by `drill.py`), or
3. `src/topics` (the default).

That's why the same test suite can grade your study workspace, a drill day, or
the reference solutions:

```bash
ALGO_TARGET=solutions uv run pytest   # sanity-check: solutions are all green
```

## Project layout

```
docs/        study these first — a concise explainer + a `*.deep.md` deep dive per topic
src/topics/  your study workspace (stubs to fill in), grouped by category
src/days/    drill scratch (created by drill.py, gitignored)
stubs/       pristine blank stubs (source of truth for drill.py — don't edit)
solutions/   worked reference implementations (peek when stuck)
tests/       pytest suite (grades whatever the active target is)
common/      shared given types (BinaryNode, graph type aliases) — not exercises
harness.py   the load() that finds your code in the active target
drill.py     reset/drill helper
```

## Topics (~27)

| Category | Topics |
|---|---|
| **search** | linear search, binary search, two crystal balls |
| **sorting** | bubble, insertion, merge, quick |
| **linked lists** | singly, doubly |
| **linear** | queue, stack, array list |
| **recursion** | maze solver |
| **trees** | pre/in/post-order, BFS, compare, DFS on BST |
| **trie** | trie (prefix tree) |
| **graphs** | DFS (adj. list), BFS (adj. matrix), Dijkstra, Prim |
| **hashing** | hash map |
| **heap** | min heap |
| **cache** | LRU |

## Suggested learning order

Work top to bottom — each builds on the last. Track yourself in
[`docs/progress.md`](docs/progress.md).

1. search → 2. sorting → 3. linked lists → 4. queue/stack/array list →
5. recursion (maze) → 6. trees → 7. trie → 8. hash map → 9. heap →
10. graphs → 11. LRU (ties together a hash map + a linked list).

New to Big-O? Read [`docs/01-big-o.md`](docs/01-big-o.md) first.

## Contributing

Want to add a topic? See [`CONTRIBUTING.md`](CONTRIBUTING.md) — each topic is
five matched files (stub, solution, test, concise doc, deep doc) and a couple of
registrations.

## License

[MIT](LICENSE) © 2026 54L1M
