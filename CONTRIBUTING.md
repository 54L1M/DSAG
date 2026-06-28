# Contributing

Thanks for wanting to extend DSAG! This is a *learning-first* repo, so the bar
for a contribution is less "clever code" and more "a clean, well-explained
exercise that teaches a concept." Most contributions add a **new topic**.

## Ground rules

- **Stubs are blank.** A stub gives the signature, type hints, and a docstring
  (with complexity) — then `raise NotImplementedError`. It must never contain a
  working implementation.
- **Solutions must be correct.** The test suite is validated against `solutions/`
  (`make test-solutions` must be all green), so a wrong solution = a wrong test.
- **Tests grade the learner, not the solution.** They import via the harness
  (`harness.load(...)`), never a hardcoded path, so the same test runs against
  `src/topics`, a drill day, or `solutions`.
- **Build the structure, don't wrap a builtin.** If the lesson is a hash map or a
  queue, implement it from nodes / buckets — don't wrap `dict` or `list.pop(0)`.
- **Keep it `ruff`-clean.** `make lint` must pass. We keep the familiar
  `Generic[T]` style (PEP 695 rewrites are intentionally disabled); line length
  is 100.

## Dev setup

```bash
make setup          # uv sync — creates .venv with pytest + ruff
make check          # ruff + the full suite
make test-solutions # the suite against the reference solutions (must be green)
```

## Adding a new topic

A topic named `foo_bar` in category `<category>` is **five matched files**:

1. **`stubs/foo_bar.py`** — the blank exercise (source of truth that `drill.py`
   copies). Signature + type hints + docstring stating time/space complexity +
   `raise NotImplementedError`.
2. **`solutions/foo_bar.py`** — a correct, readable reference implementation.
3. **`tests/test_foo_bar.py`** — pytest cases. Start with
   `from harness import load` then `m = load("foo_bar")`, and assert against
   `m.foo_bar(...)` / `m.FooBar(...)`. Reuse helpers in `tests/_fixtures.py`
   (tree/graph builders, validators). Cover edge cases (empty, single,
   duplicates, not-found, errors) and, for things with an obvious oracle, a
   randomized check against a known-good baseline (e.g. `sorted`).
4. **`docs/<category>/foo_bar.md`** — the concise explainer (intuition → how it
   works with a small trace → complexity → pitfalls → "your task"). Match the
   header format of the existing docs.
5. **`docs/<category>/foo_bar.deep.md`** — the in-depth companion (mental model →
   invariant → detailed walkthrough → derived complexity → edge cases →
   variations → connections → self-check → common bugs). Cross-link it from the
   concise doc with the `📚 Need more detail?` line.

Then:

- **Prefill the study workspace:** copy the stub to
  `src/topics/<category>/foo_bar.py` (that's what you actually edit while
  practicing).
- **Shared types** (e.g. a node or graph alias) go in `common/types.py` — they
  are *given*, not implemented by the learner.
- **Register it:** add a row to the topic table in `README.md` and a line in
  `docs/progress.md`.

### Conventions for the contract

- Return an index or `-1` for searches; return `None` (not raise) for
  pop/peek/get-on-empty where that's the natural API; raise `IndexError` for
  out-of-range positional access.
- Document complexity in the stub docstring (`Time: O(...)  Space: O(...)`).
- Sorting and other in-place operations should say so and return `None`;
  operations that return a new collection should say *that*.

## Verifying your contribution

```bash
make test-solutions k=foo_bar   # your solution passes your tests
make test k=foo_bar             # fails with NotImplementedError on the blank stub (expected)
make lint                       # clean
```

A topic is "done" when its solution is green, its blank stub fails cleanly, ruff
passes, and both docs read well.

## Style for docs

- Python examples only; small, concrete traces; ASCII diagrams for pointer/tree/
  graph structures.
- Don't paste a full solution into a doc — explain with prose, pseudocode, and
  fragments so the exercise stays worth doing.

## License

By contributing, you agree your contributions are licensed under the project's
[MIT License](LICENSE).
