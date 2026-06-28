# How to use this gym

A short guide to getting the most out of the practice loop.

## The loop, per topic

1. **Read the doc.** Each topic has a concise explainer under `docs/<category>/`.
   Read it until you can explain the idea out loud without looking — *then* code.
   Want more? Every topic also has an in-depth `<name>.deep.md` companion
   (invariants, derived complexity, edge cases, variations, self-check
   questions) — reach for it whenever the concise version isn't enough.
2. **Look at the stub.** Open `src/topics/<category>/<name>.py`. The signature,
   type hints, and docstring tell you exactly what to build. Don't change the
   signature — the tests rely on it.
3. **Implement.** Delete the `raise NotImplementedError` and write the body.
4. **Run the test.** `uv run pytest -k <name>` runs just that topic. Red →
   read the failure, fix, repeat. Green → you've got it.
5. **Compare.** Open `solutions/<name>.py` and diff your approach against the
   reference. Different but passing is fine — there's rarely one right answer.

## When you're stuck

- Re-read the doc's "How it works" and "Common pitfalls" sections.
- Add `print()`s or run `uv run pytest -k <name> -s` to see them.
- Write the algorithm on paper with a tiny input (3–4 elements) by hand first.
- Only then peek at the solution — and if you do, close it and re-implement
  from memory afterwards.

## Drilling (spaced repetition)

Understanding a thing once ≠ being able to write it under pressure. After you've
solved a topic, come back days later and redo it cold:

```bash
uv run python drill.py     # blank copies of everything in src/days/dayN
uv run pytest -k <name>    # redo a topic from scratch
```

Aim to get each topic to where you can write it correctly, from a blank file,
in a few minutes. That's the real goal.

## Tips

- `uv run pytest -q` for terse output; add `-x` to stop at the first failure.
- The 5-second per-test timeout (in `pyproject.toml`) catches infinite loops —
  if a test "times out", you probably have a loop that never advances.
- Keep your code `ruff`-clean (`uv run ruff check`); good habits compound.
- Mark your progress in [`progress.md`](progress.md).
