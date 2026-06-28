---
name: Bug report
about: A solution, test, doc, or tool is wrong or broken
title: "[bug] "
labels: bug
---

## What's wrong?

<!-- One or two sentences. Which topic / file? -->

## Where

- [ ] A reference solution in `solutions/`
- [ ] A test in `tests/`
- [ ] A doc (`docs/...`, concise or `.deep.md`)
- [ ] Tooling (`harness.py`, `drill.py`, `bench.py`, `Makefile`)
- [ ] Other:

Topic / file: <!-- e.g. graphs/dijkstra -->

## Expected vs. actual

<!-- What you expected, and what happened instead. -->

## To reproduce

```bash
# the command you ran, e.g.
make test-solutions k=dijkstra
```

<!-- Paste the relevant output / traceback. -->

## Environment

- OS:
- Python (`uv run python --version`):
- `uv --version`:
